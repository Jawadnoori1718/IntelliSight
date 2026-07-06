import { useRef } from 'react'
import { useApp } from '../context/AppContext'
import { useElementSize } from '../hooks/useElementSize'
import { useTrackedDetections } from '../hooks/useTrackedDetections'

/**
 * Draws animated bounding boxes over the live video.
 *
 * The video uses object-fit: cover, so we replicate that cover transform to map
 * each detection's normalised (0..1) box onto the exact on-screen position.
 */
export default function DetectionOverlay() {
  const { videoRef, detections, cameraStatus } = useApp()
  const live = cameraStatus === 'live'
  const tracked = useTrackedDetections(detections, live)
  const containerRef = useRef(null)
  const { w, h } = useElementSize(containerRef)

  const video = videoRef.current
  const vw = video?.videoWidth || 0
  const vh = video?.videoHeight || 0

  let boxes = []
  if (vw && vh && w && h) {
    // Match object-fit: cover — scale to fill, centre, and crop the overflow.
    const scale = Math.max(w / vw, h / vh)
    const renderW = vw * scale
    const renderH = vh * scale
    const offsetX = (w - renderW) / 2
    const offsetY = (h - renderH) / 2

    boxes = tracked.map((t) => ({
      ...t,
      px: {
        x: offsetX + t.box.x1 * renderW,
        y: offsetY + t.box.y1 * renderH,
        w: (t.box.x2 - t.box.x1) * renderW,
        h: (t.box.y2 - t.box.y1) * renderH,
      },
    }))
  }

  if (!live) return null

  return (
    <div className="det-overlay" ref={containerRef}>
      {boxes.map((b) => (
        <div
          key={b.id}
          className="det-anchor"
          style={{ transform: `translate(${b.px.x}px, ${b.px.y}px)`, width: b.px.w, height: b.px.h }}
        >
          <div className={`det-box cat-${b.category} ${b.px.y < 26 ? 'label-below' : ''}`}>
            <span className="det-label">
              <span className="det-name">{b.label}</span>
              <span className="det-conf">{Math.round(b.confidence * 100)}%</span>
            </span>
          </div>
        </div>
      ))}
    </div>
  )
}
