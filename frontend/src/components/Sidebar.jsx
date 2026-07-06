import { useState } from 'react'
import { Boxes, MessageSquare, Clock, Brain, Search, Sparkles, Mic } from 'lucide-react'
import ScenePanel from './panels/ScenePanel'
import ObjectsPanel from './panels/ObjectsPanel'
import AssistantPanel from './panels/AssistantPanel'
import TimelinePanel from './panels/TimelinePanel'
import MemoryPanel from './panels/MemoryPanel'
import SearchPanel from './panels/SearchPanel'
import InsightsPanel from './panels/InsightsPanel'

const TABS = [
  { id: 'objects', label: 'Objects', icon: Boxes, Panel: ObjectsPanel },
  { id: 'assistant', label: 'Assistant', icon: MessageSquare, Panel: AssistantPanel },
  { id: 'timeline', label: 'Timeline', icon: Clock, Panel: TimelinePanel },
  { id: 'memory', label: 'Memory', icon: Brain, Panel: MemoryPanel },
  { id: 'search', label: 'Search', icon: Search, Panel: SearchPanel },
  { id: 'insights', label: 'Insights', icon: Sparkles, Panel: InsightsPanel },
]

export default function Sidebar() {
  const [active, setActive] = useState('objects')
  const ActivePanel = TABS.find((t) => t.id === active).Panel

  return (
    <aside className="sidebar">
      <ScenePanel />

      <nav className="tabs">
        {TABS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            className={`tab ${active === id ? 'tab-active' : ''}`}
            onClick={() => setActive(id)}
            title={label}
          >
            <Icon size={18} />
            <span>{label}</span>
          </button>
        ))}
      </nav>

      <div className="panel-scroll">
        <ActivePanel />
      </div>

      <div className="ask-bar glass">
        <input placeholder="Ask about what you see…" disabled />
        <button className="mic-btn" title="Voice assistant (Phase 14)" aria-label="Voice">
          <Mic size={18} />
        </button>
      </div>
    </aside>
  )
}
