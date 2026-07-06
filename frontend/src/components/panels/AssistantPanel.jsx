import { Sparkles } from 'lucide-react'

export default function AssistantPanel() {
  return (
    <div className="panel glass">
      <div className="panel-head">
        <h3>AI Assistant</h3>
        <span className="tag">preview</span>
      </div>

      <div className="chat">
        <div className="msg user">What am I looking at?</div>
        <div className="msg ai">
          <Sparkles size={14} />
          <span>
            A desk workspace — a laptop, coffee mug, keyboard and notebook. It looks like an
            active work session.
          </span>
        </div>
      </div>

      <p className="soon">💬 Live question &amp; answer arrives in Phase 13.</p>
    </div>
  )
}
