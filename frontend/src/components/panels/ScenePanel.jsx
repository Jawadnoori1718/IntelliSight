import { sampleScene as s } from '../../data/placeholders'

function SceneStat({ label, value }) {
  return (
    <div className="scene-stat">
      <span>{label}</span>
      <b>{value}</b>
    </div>
  )
}

export default function ScenePanel() {
  return (
    <div className="panel scene-panel glass">
      <div className="panel-head">
        <h3>Current Scene</h3>
        <span className="tag">sample</span>
      </div>

      <p className="scene-desc">{s.description}</p>

      <div className="scene-grid">
        <SceneStat label="Activity" value={s.activity} />
        <SceneStat label="Environment" value={s.environment} />
        <SceneStat label="Lighting" value={s.lighting} />
        <SceneStat label="Desk" value={s.desk} />
      </div>

      <div className="scene-conf">
        <span>Confidence</span>
        <div className="conf-bar">
          <div className="conf-fill" style={{ width: `${s.confidence * 100}%` }} />
        </div>
        <b>{Math.round(s.confidence * 100)}%</b>
      </div>
    </div>
  )
}
