import { createContext, useContext, useRef, useState, useCallback, useEffect } from 'react'
import { useDetectionStream } from '../hooks/useDetectionStream'

/**
 * Shared IntelliSight app state.
 *
 * Owns the webcam (video ref, status, start/stop) and the live object
 * detections streamed from the backend. Later phases extend this context.
 */
const AppContext = createContext(null)

// Turn a raw getUserMedia error into a friendly, actionable message.
function describeCameraError(err) {
  switch (err?.name) {
    case 'NotAllowedError':
    case 'SecurityError':
      return 'Camera access was blocked. Click the camera icon in your browser’s address bar, allow access, then try again.'
    case 'NotFoundError':
    case 'OverconstrainedError':
      return 'No camera was found. Make sure a webcam is connected.'
    case 'NotReadableError':
      return 'Your camera is already in use by another app (Zoom, FaceTime, etc.). Close it and try again.'
    default:
      return 'Something went wrong starting the camera. Please try again.'
  }
}

const EMPTY_META = { connected: false, fps: 0, latencyMs: 0, inferenceMs: 0, cpu: 0, spark: [] }

export function AppProvider({ children }) {
  const videoRef = useRef(null)
  const streamRef = useRef(null)

  // idle | starting | live | error
  const [cameraStatus, setCameraStatus] = useState('idle')
  const [cameraError, setCameraError] = useState(null)

  // Live object detection
  const [detections, setDetections] = useState([])
  const [detectionMeta, setDetectionMeta] = useState(EMPTY_META)

  const startCamera = useCallback(async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraStatus('error')
      setCameraError('Camera access isn’t available here. Use a modern browser on http://localhost or an https page.')
      return
    }

    setCameraError(null)
    setCameraStatus('starting')

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' },
        audio: false,
      })
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        await videoRef.current.play().catch(() => {})
      }
      setCameraStatus('live')
    } catch (err) {
      setCameraStatus('error')
      setCameraError(describeCameraError(err))
    }
  }, [])

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
      streamRef.current = null
    }
    if (videoRef.current) videoRef.current.srcObject = null
    setCameraStatus('idle')
  }, [])

  // Release the camera when the app unmounts.
  useEffect(() => () => stopCamera(), [stopCamera])

  // Stream frames to the backend and collect detections while live.
  const handleResult = useCallback(({ detections: dets, latencyMs, fps, inferenceMs, cpu, spark }) => {
    setDetections(dets)
    setDetectionMeta({ connected: true, fps, latencyMs, inferenceMs, cpu, spark })
  }, [])
  const handleStatus = useCallback((connected) => {
    setDetectionMeta((meta) => ({ ...meta, connected }))
  }, [])

  useDetectionStream({
    videoRef,
    enabled: cameraStatus === 'live',
    onResult: handleResult,
    onStatus: handleStatus,
  })

  // Clear detections whenever we leave the live state.
  useEffect(() => {
    if (cameraStatus !== 'live') {
      setDetections([])
      setDetectionMeta(EMPTY_META)
    }
  }, [cameraStatus])

  const value = {
    videoRef,
    cameraStatus,
    cameraError,
    startCamera,
    stopCamera,
    detections,
    detectionMeta,
  }
  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within <AppProvider>')
  return ctx
}
