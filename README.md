# 👁️ IntelliSight

### An AI-powered real-time visual intelligence assistant that understands the world through your camera.

IntelliSight doesn't just **detect** objects — it **analyses, understands, explains, remembers, and interacts** with your surroundings in real time.

---

## ✨ What makes it different

A normal object detector shows you this:

```
Person
Laptop
Bottle
Chair
```

**IntelliSight** shows you this:

```
Person          → Software Developer
Laptop          → MacBook Pro 14"
Bottle          → Coffee Mug (ceramic, ~350ml)
...

CURRENT SCENE
A person is working at a desk.
Detected Objects: 9   ·   Activity: Working   ·   Environment: Office
Lighting: Bright      ·   Desk Status: Organised   ·   Confidence: 97%
```

It should make people say *"That's an AI that understands what it's seeing"* — not *"that's an object detector."*

---

## 🚀 Core Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Live Object Detection** | Animated boxes, clean labels, confidence + category colours |
| 2 | **OCR** | Reads any text — books, screens, whiteboards, signs, labels |
| 3 | **AI Explanations** | Context for every object, not just a label |
| 4 | **Ask Questions** | "What's on my desk?", "How many bottles?", "Read that sign." |
| 5 | **Scene Understanding** | A human-like description of the whole scene |
| 6 | **Memory Mode** | "Where did I leave my phone?" → last seen location + time |
| 7 | **Smart Search** | Search your visual history |
| 8 | **Smart OCR** | Read → summarise → translate → answer questions |
| 9 | **Object Relationships** | Understands space: "phone is right of the laptop" |
| 10 | **Live Statistics** | FPS, objects, people, confidence, latency |
| 11 | **AI Knowledge Cards** | Click any object for a rich info panel |
| 12 | **Voice Assistant** | Talk naturally, it answers |
| 13 | **Visual Timeline** | Every detection, searchable + jump-to-frame |
| 14 | **AI Insights** | Observations with confidence, not just certainties |

---

## 🎨 The Interface

Closer to a **futuristic operating system** than a school project:

- 🌑 Dark theme
- 🧊 Glassmorphism
- 💙 Neon blue accents
- 🎞️ Smooth animations
- ▭ Rounded panels
- 🧘 Minimalist design

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React + Vite (dark glassmorphism UI) |
| **Backend** | Python + FastAPI |
| **Object Detection** | Ultralytics YOLO |
| **OCR** | EasyOCR |
| **AI Brain** | Claude (multimodal) for understanding, explanations & Q&A |
| **Realtime** | WebSockets (low-latency detection stream) |

---

## 🏗️ Architecture (at a glance)

```
  Browser (React)                    FastAPI Backend
  ┌────────────────────┐             ┌──────────────────────────┐
  │  Webcam capture     │  frames    │  YOLO   → objects         │
  │  Canvas overlays    │ ─────────► │  EasyOCR → text           │
  │  Glassmorphism UI   │ ◄───────── │  Claude  → understanding  │
  │  Voice in / out     │  results   │  Memory  → timeline/search │
  └────────────────────┘  (WebSocket)└──────────────────────────┘
```

---

## 📦 Project Status

🚧 **Under active construction — built in 20 phases.**
See the full plan and progress in **[docs/ROADMAP.md](docs/ROADMAP.md)**.

- [x] **Phase 1** — Foundation & Repo Setup
- [x] **Phase 2** — Backend Skeleton (FastAPI + `/health`)
- [ ] Phases 3–20 — coming next

**Run the backend:** see **[backend/README.md](backend/README.md)** (`cd backend`, create the venv, `./run.sh`, then open http://127.0.0.1:8000/health). The frontend arrives in Phase 3.

---

## 📄 License

[MIT](LICENSE)
