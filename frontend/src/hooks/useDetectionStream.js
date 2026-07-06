import { useEffect, useRef } from 'react'

// Tuning knobs for the realtime detection stream.
const CAPTURE_WIDTH = 640 // downscale frames before sending (speed)
const JPEG_QUALITY = 0.6
const MIN_FRAME_GAP_MS = 120 // don't send faster than this

/**
 * Streams webcam frames to the backend for object detection.
 *
 * While `enabled`, it opens a WebSocket to /ws/detect and runs a
 * request→response loop: send a frame, wait for the detections, then send the
 * next one. This naturally throttles to whatever speed the backend can manage.
 */
export function useDetectionStream({ videoRef, enabled, onResult, onStatus }) {
  // Keep the latest callbacks in refs so the socket effect doesn't re-run.
  const onResultRef = useRef(onResult)
  const onStatusRef = useRef(onStatus)
  onResultRef.current = onResult
  onStatusRef.current = onStatus

  useEffect(() => {
    if (!enabled) return

    let closed = false
    let sentAt = 0
    const frameTimes = []

    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const ws = new WebSocket(`${proto}://${window.location.host}/ws/detect`)
    ws.binaryType = 'arraybuffer'

    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')

    const captureAndSend = () => {
      if (closed) return
      const video = videoRef.current
      if (!video || video.readyState < 2 || ws.readyState !== WebSocket.OPEN) return
      const vw = video.videoWidth
      const vh = video.videoHeight
      if (!vw || !vh) return

      canvas.width = CAPTURE_WIDTH
      canvas.height = Math.round((vh / vw) * CAPTURE_WIDTH)
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      canvas.toBlob(
        (blob) => {
          if (!blob || closed || ws.readyState !== WebSocket.OPEN) return
          blob.arrayBuffer().then((buf) => {
            if (closed || ws.readyState !== WebSocket.OPEN) return
            sentAt = performance.now()
            ws.send(buf)
          })
        },
        'image/jpeg',
        JPEG_QUALITY,
      )
    }

    ws.onopen = () => {
      onStatusRef.current?.(true)
      captureAndSend()
    }
    ws.onclose = () => onStatusRef.current?.(false)
    ws.onerror = () => onStatusRef.current?.(false)
    ws.onmessage = (event) => {
      const now = performance.now()
      const latencyMs = Math.round(now - sentAt)

      // Rolling frames-per-second over the last second.
      frameTimes.push(now)
      while (frameTimes.length && now - frameTimes[0] > 1000) frameTimes.shift()

      let data
      try {
        data = JSON.parse(event.data)
      } catch {
        return
      }
      onResultRef.current?.({
        detections: data.detections || [],
        latencyMs,
        fps: frameTimes.length,
      })

      const wait = Math.max(0, MIN_FRAME_GAP_MS - (now - sentAt))
      window.setTimeout(captureAndSend, wait)
    }

    return () => {
      closed = true
      try {
        ws.close()
      } catch {
        /* ignore */
      }
    }
  }, [enabled, videoRef])
}
