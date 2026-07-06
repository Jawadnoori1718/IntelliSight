import { useApp } from '../../context/AppContext'
import { sampleObjects } from '../../data/placeholders'

export default function ObjectsPanel() {
  const { detections, cameraStatus } = useApp()
  const live = cameraStatus === 'live'
  const items = live ? detections : sampleObjects

  return (
    <div className="panel glass">
      <div className="panel-head">
        <h3>Detected Objects</h3>
        <span className="count-pill">{items.length}</span>
      </div>

      {live && items.length === 0 ? (
        <p className="empty-note">Scanning your surroundings… point your camera at some objects.</p>
      ) : (
        <ul className="obj-list">
          {items.map((o, i) => (
            <li className="obj" key={o.id ?? i}>
              <span className={`obj-dot cat-${o.category}`} />
              <div className="obj-main">
                <div className="obj-label">
                  {o.label}
                  {o.sub ? <span className="obj-sub"> {o.sub}</span> : null}
                </div>
                <div className="obj-bar">
                  <div className="obj-bar-fill" style={{ width: `${o.confidence * 100}%` }} />
                </div>
              </div>
              <span className="obj-conf">{Math.round(o.confidence * 100)}%</span>
            </li>
          ))}
        </ul>
      )}

      {!live && <p className="soon">📷 Start the camera to see live detections here.</p>}
    </div>
  )
}
