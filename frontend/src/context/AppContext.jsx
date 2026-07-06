import { createContext, useContext, useRef, useState, useCallback, useEffect } from 'react'

/**
 * Shared IntelliSight app state.
 *
 * For now it owns the webcam: the <video> ref, the camera status and any error,
 * plus start/stop controls. Later phases (detection, stats, scene, memory…) will
 * extend this same context.
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

export function AppProvider({ children }) {
  const videoRef = useRef(null)
  const streamRef = useRef(null)

  // idle | starting | live | error
  const [cameraStatus, setCameraStatus] = useState('idle')
  const [cameraError, setCameraError] = useState(null)

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

  const value = { videoRef, cameraStatus, cameraError, startCamera, stopCamera }
  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within <AppProvider>')
  return ctx
}
