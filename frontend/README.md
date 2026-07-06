# IntelliSight — Frontend

The **React + Vite** web interface — the part people see and say *"wow"* about.

- 🌑 Dark theme · 🧊 glassmorphism · 💙 neon blue accents
- 📷 Live webcam capture in the browser *(Phase 4)*
- ▭ Animated detection overlays on a canvas *(Phase 6)*
- 📊 Live statistics dashboard
- 🗨️ Scene, Objects, Assistant, Timeline, Memory, Search & Insights panels

---

## 🚀 Quick start

```bash
cd ~/Desktop/IntelliSight/frontend
npm install
npm run dev
```

Then open **http://localhost:5173** in your browser.

> Right now the panels show tastefully styled **sample data** (tagged “sample”/“preview”)
> so the interface feels alive. Real camera + detection data flows in from Phase 4 onward.

### Build for production

```bash
npm run build      # outputs to dist/
npm run preview    # preview the production build
```

---

## 🗂️ Structure

```
frontend/
├── index.html
├── vite.config.js          # dev server + /api & /ws proxy to the backend
└── src/
    ├── main.jsx            # entry point
    ├── App.jsx            # top-level layout
    ├── styles/            # theme (tokens) + layout + panels CSS
    ├── data/              # sample placeholder data
    └── components/
        ├── Header.jsx
        ├── CameraStage.jsx
        ├── StatsDashboard.jsx
        ├── Sidebar.jsx
        └── panels/        # Scene, Objects, Assistant, Timeline, Memory, Search, Insights
```

> 🚧 See [`../docs/ROADMAP.md`](../docs/ROADMAP.md) for what each phase adds.
