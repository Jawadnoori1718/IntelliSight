import { Activity, Boxes, Users, Type, Gauge, Timer, Zap, Cpu } from 'lucide-react'
import { useApp } from '../context/AppContext'

// A tiny stretched-to-fit activity sparkline (objects detected over time).
function Sparkline({ data }) {
  if (!data || data.length < 2) {
    return <div className="spark-empty" />
  }
  const max = Math.max(1, ...data)
  const stepX = 100 / (data.length - 1)
  const points = data.map((v, i) => [i * stepX, 30 - (v / max) * 26 - 2])
  const line = points.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`).join(' ')
  const area = `${line} L100,30 L0,30 Z`

  return (
    <svg className="spark" viewBox="0 0 100 30" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.35" />
          <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
        </linearGradient>
      </defs>
      <path className="spark-area" d={area} />
      <path className="spark-line" d={line} />
    </svg>
  )
}

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
    { icon: Timer, label: 'Response', value: live && detectionMeta.latencyMs ? `${detectionMeta.latencyMs}ms` : '—' },
    { icon: Zap, label: 'Inference', value: live && detectionMeta.inferenceMs ? `${detectionMeta.inferenceMs}ms` : '—' },
    { icon: Cpu, label: 'CPU', value: live && detectionMeta.cpu ? `${detectionMeta.cpu}%` : '—' },
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

      <div className="spark-wrap">
        <div className="spark-label">
          <span>Activity</span>
          <span>{live ? `${detections.length} now` : 'idle'}</span>
        </div>
        {live ? <Sparkline data={detectionMeta.spark} /> : <div className="spark-empty" />}
      </div>
    </div>
  )
}
