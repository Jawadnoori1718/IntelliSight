import { Camera } from 'lucide-react'
import StatsDashboard from './StatsDashboard'

export default function CameraStage() {
  return (
    <section className="stage glass">
      <StatsDashboard />

      <div className="stage-placeholder">
        <div className="stage-icon">
          <Camera size={48} strokeWidth={1.5} />
        </div>
        <h2>Camera feed appears here</h2>
        <p>
          Live webcam &amp; detection overlays arrive in <b>Phase 4</b>.
        </p>
      </div>

      <div className="scanline" />
      <span className="corner tl" />
      <span className="corner tr" />
      <span className="corner bl" />
      <span className="corner br" />
    </section>
  )
}
