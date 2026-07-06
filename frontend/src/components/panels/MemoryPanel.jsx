import { sampleMemory } from '../../data/placeholders'

export default function MemoryPanel() {
  return (
    <div className="panel glass">
      <div className="panel-head">
        <h3>Memory</h3>
        <span className="tag">sample</span>
      </div>

      <ul className="memory">
        {sampleMemory.map((m, i) => (
          <li className="mem-item" key={i}>
            <span className="mem-time">{m.time}</span>
            <div>
              <div className="mem-text">{m.text}</div>
              <div className="mem-where">{m.where}</div>
            </div>
          </li>
        ))}
      </ul>

      <p className="soon">🧠 “Where did I leave my…?” arrives in Phase 15.</p>
    </div>
  )
}
