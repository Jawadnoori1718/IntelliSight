import { Search } from 'lucide-react'

const EXAMPLES = ['Find my wallet', 'Show every book', 'Red objects', 'When did I last see my phone?']

export default function SearchPanel() {
  return (
    <div className="panel glass">
      <div className="panel-head">
        <h3>Smart Search</h3>
      </div>

      <div className="search-box">
        <Search size={16} />
        <input placeholder="Search your visual history…" disabled />
      </div>

      <div className="chips">
        {EXAMPLES.map((e) => (
          <span className="chip" key={e}>
            {e}
          </span>
        ))}
      </div>

      <p className="soon">🔎 Visual history search arrives in Phase 16.</p>
    </div>
  )
}
