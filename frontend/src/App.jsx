import Header from './components/Header'
import CameraStage from './components/CameraStage'
import Sidebar from './components/Sidebar'

export default function App() {
  return (
    <div className="app">
      <Header />
      <main className="workspace">
        <CameraStage />
        <Sidebar />
      </main>
    </div>
  )
}
