import { Camera, CameraOff, Loader2, Square } from 'lucide-react'
import { useApp } from '../context/AppContext'
import StatsDashboard from './StatsDashboard'

export default function CameraStage() {
  const { videoRef, cameraStatus, cameraError, startCamera, stopCamera } = useApp()
  const isLive = cameraStatus === 'live'

  return (
    <section className="stage glass">
      <StatsDashboard />

      {/* The live video always exists so the ref is attached; it fades in when live. */}
      <video
        ref={videoRef}
        className={`stage-video ${isLive ? 'is-live' : ''}`}
        autoPlay
        muted
        playsInline
      />

      {!isLive && (
        <div className="stage-placeholder">
          {cameraStatus === 'idle' && (
            <>
              <div className="stage-icon">
                <Camera size={48} strokeWidth={1.5} />
              </div>
              <h2>Camera feed appears here</h2>
              <p>Turn on your webcam to bring IntelliSight to life.</p>
              <button className="btn-primary" onClick={startCamera}>
                <Camera size={16} /> Start Camera
              </button>
            </>
          )}

          {cameraStatus === 'starting' && (
            <>
              <div className="stage-icon spinning">
                <Loader2 size={44} strokeWidth={1.6} />
              </div>
              <h2>Requesting camera…</h2>
              <p>Please allow camera access in your browser.</p>
            </>
          )}

          {cameraStatus === 'error' && (
            <>
              <div className="stage-icon error">
                <CameraOff size={44} strokeWidth={1.5} />
              </div>
              <h2>Couldn’t start the camera</h2>
              <p>{cameraError}</p>
              <button className="btn-primary" onClick={startCamera}>
                <Camera size={16} /> Try again
              </button>
            </>
          )}
        </div>
      )}

      {isLive && (
        <button className="stage-stop" onClick={stopCamera} title="Stop camera">
          <Square size={13} /> Stop
        </button>
      )}

      <div className="scanline" />
      <span className="corner tl" />
      <span className="corner tr" />
      <span className="corner bl" />
      <span className="corner br" />
    </section>
  )
}
