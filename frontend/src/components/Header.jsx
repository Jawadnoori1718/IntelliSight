import { Eye, Settings } from 'lucide-react'
import { useApp } from '../context/AppContext'

// Map the camera status to the little status pill in the header.
const STATUS = {
  idle: { cls: 'pill-standby', label: 'STANDBY' },
  starting: { cls: 'pill-standby', label: 'CONNECTING' },
  live: { cls: 'pill-live', label: 'LIVE' },
  error: { cls: 'pill-error', label: 'OFFLINE' },
}

export default function Header() {
  const { cameraStatus } = useApp()
  const status = STATUS[cameraStatus] ?? STATUS.idle

  return (
    <header className="header glass">
      <div className="brand">
        <div className="brand-logo">
          <Eye size={22} strokeWidth={2.2} />
        </div>
        <div className="brand-text">
          <h1>IntelliSight</h1>
          <span>Visual Intelligence</span>
        </div>
      </div>

      <div className="header-status">
        <div className={`pill ${status.cls}`}>
          <span className="dot" />
          {status.label}
        </div>
        <button className="icon-btn" title="Settings" aria-label="Settings">
          <Settings size={18} />
        </button>
      </div>
    </header>
  )
}
