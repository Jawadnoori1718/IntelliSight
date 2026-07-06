import { Activity, Boxes, Users, Type, Gauge, Timer, Cpu, Zap } from 'lucide-react'
import { useApp } from '../context/AppContext'

export default function StatsDashboard() {
  const { detections, detectionMeta, cameraStatus } = useApp()
  const live = cameraStatus === 'live'

  const people = detections.filter((d) => d.category === 'person').length
  const avgConf = detections.length
    ? Math.round((detections.reduce((sum, d) => sum + d.confidence, 0) / detections.length) * 100)
    : null

  const stats = [
    { icon: Activity, label: 'FPS', value: live ? String(detectionMeta.fps) : '—' },
    { icon: Boxes, label: 'Objects', value: live ? String(detections.length) : '0' },
    { icon: Users, label: 'People', value: live ? String(people) : '0' },
    { icon: Type, label: 'Text', value: '0' },
    { icon: Gauge, label: 'Confidence', value: live && avgConf != null ? `${avgConf}%` : '—' },
    { icon: Timer, label: 'Latency', value: live && detectionMeta.latencyMs ? `${detectionMeta.latencyMs}ms` : '—' },
    { icon: Cpu, label: 'CPU', value: '—' },
    { icon: Zap, label: 'GPU', value: '—' },
  ]

  return (
    <div className="stats glass-strong">
      <div className="stats-title">
        <span className={`live-dot ${live ? 'on' : ''}`} />
        LIVE STATS
      </div>
      <div className="stats-grid">
        {stats.map(({ icon: Icon, label, value }) => (
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
