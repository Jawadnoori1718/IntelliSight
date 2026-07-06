import { Activity, Boxes, Users, Type, Gauge, Timer, Cpu, Zap } from 'lucide-react'

// Placeholder values until live detection streams in (Phase 5–7).
const STATS = [
  { icon: Activity, label: 'FPS', value: '—' },
  { icon: Boxes, label: 'Objects', value: '0' },
  { icon: Users, label: 'People', value: '0' },
  { icon: Type, label: 'Text', value: '0' },
  { icon: Gauge, label: 'Confidence', value: '—' },
  { icon: Timer, label: 'Latency', value: '—' },
  { icon: Cpu, label: 'CPU', value: '—' },
  { icon: Zap, label: 'GPU', value: '—' },
]

export default function StatsDashboard() {
  return (
    <div className="stats glass-strong">
      <div className="stats-title">
        <span className="live-dot" />
        LIVE STATS
      </div>
      <div className="stats-grid">
        {STATS.map(({ icon: Icon, label, value }) => (
          <div className="stat" key={label}>
            <Icon size={15} className="stat-icon" />
            <div>
              <div className="stat-value">{value}</div>
              <div className="stat-label">{label}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
