import { useEffect, useRef, useState } from 'react'

// Lightweight frame-to-frame tracking so each box keeps a stable identity
// (and therefore glides smoothly via CSS transitions) instead of flickering.
const IOU_MATCH = 0.25 // minimum overlap to consider two boxes "the same object"
const MAX_MISSES = 1 // keep a briefly-lost box for this many frames before dropping

function iou(a, b) {
  const x1 = Math.max(a.x1, b.x1)
  const y1 = Math.max(a.y1, b.y1)
  const x2 = Math.min(a.x2, b.x2)
  const y2 = Math.min(a.y2, b.y2)
  const inter = Math.max(0, x2 - x1) * Math.max(0, y2 - y1)
  const areaA = (a.x2 - a.x1) * (a.y2 - a.y1)
  const areaB = (b.x2 - b.x1) * (b.y2 - b.y1)
  const union = areaA + areaB - inter
  return union > 0 ? inter / union : 0
}

export function useTrackedDetections(detections, enabled) {
  const tracked = useRef([])
  const nextId = useRef(0)
  const [output, setOutput] = useState([])

  useEffect(() => {
    if (!enabled) {
      tracked.current = []
      setOutput([])
      return
    }

    const prev = tracked.current
    const used = new Set()
    const next = []

    // Match each detection to the best unused previous track with the same label.
    for (const det of detections) {
      let best = -1
      let bestScore = IOU_MATCH
      for (let i = 0; i < prev.length; i++) {
        if (used.has(i) || prev[i].label !== det.label) continue
        const score = iou(prev[i].box, det.box)
        if (score >= bestScore) {
          bestScore = score
          best = i
        }
      }

      if (best >= 0) {
        used.add(best)
        next.push({ id: prev[best].id, ...det, misses: 0 })
      } else {
        nextId.current += 1
        next.push({ id: `d${nextId.current}`, ...det, misses: 0 })
      }
    }

    // Keep momentarily-lost tracks for a frame so they don't blink out.
    for (let i = 0; i < prev.length; i++) {
      if (!used.has(i) && prev[i].misses < MAX_MISSES) {
        next.push({ ...prev[i], misses: prev[i].misses + 1 })
      }
    }

    tracked.current = next
    setOutput(next)
  }, [detections, enabled])

  return output
}
