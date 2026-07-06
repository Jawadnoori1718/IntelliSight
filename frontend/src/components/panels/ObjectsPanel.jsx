import { sampleObjects } from '../../data/placeholders'

export default function ObjectsPanel() {
  return (
    <div className="panel glass">
      <div className="panel-head">
        <h3>Detected Objects</h3>
        <span className="count-pill">{sampleObjects.length}</span>
      </div>

      <ul className="obj-list">
        {sampleObjects.map((o) => (
          <li className="obj" key={o.id}>
            <span className={`obj-dot cat-${o.category}`} />
            <div className="obj-main">
              <div className="obj-label">
                {o.label} <span className="obj-sub">{o.sub}</span>
              </div>
              <div className="obj-bar">
                <div className="obj-bar-fill" style={{ width: `${o.confidence * 100}%` }} />
              </div>
            </div>
            <span className="obj-conf">{Math.round(o.confidence * 100)}%</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
