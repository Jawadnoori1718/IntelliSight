import { sampleTimeline } from '../../data/placeholders'

export default function TimelinePanel() {
  return (
    <div className="panel glass">
      <div className="panel-head">
        <h3>Timeline</h3>
        <span className="tag">sample</span>
      </div>

      <ul className="timeline">
        {sampleTimeline.map((t, i) => (
          <li className="tl-item" key={i}>
            <span className="tl-time">{t.time}</span>
            <span className={`tl-dot cat-${t.category}`} />
            <span className="tl-label">{t.label}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
