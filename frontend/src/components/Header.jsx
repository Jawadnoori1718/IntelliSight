import { Eye, Settings } from 'lucide-react'

export default function Header() {
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
        <div className="pill pill-standby">
          <span className="dot" />
          STANDBY
        </div>
        <button className="icon-btn" title="Settings" aria-label="Settings">
          <Settings size={18} />
        </button>
      </div>
    </header>
  )
}
