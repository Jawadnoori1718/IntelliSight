import { sampleInsights } from '../../data/placeholders'

export default function InsightsPanel() {
  return (
    <div className="panel glass">
      <div className="panel-head">
        <h3>AI Insights</h3>
        <span className="tag">sample</span>
      </div>

      <ul className="insights">
        {sampleInsights.map((it, i) => (
          <li className="insight" key={i}>
            <span className="insight-dot" />
            <span className="insight-text">{it.text}</span>
            <span className="insight-conf">{Math.round(it.confidence * 100)}%</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
