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
| **Desktop app** *(current)* | PySide6 / Qt — native window with QPainter segmentation overlays |
| **Frontend** *(web v1)* | React + Vite (dark glassmorphism UI) |
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

IntelliSight now has **two editions**:

### 🖥️ Desktop Edition — *current focus*
A **native Mac app** (PySide6) with super-accurate object **segmentation** — coloured
outlines around everything it sees. Built in 12 phases (see **[docs/ROADMAP.md](docs/ROADMAP.md)**).

- [x] **D1** — Desktop app window + dark UI shell
- [x] **D2** — Live camera in the window
- [x] **D3** — Accurate vision engine (YOLO11-seg on Apple GPU)
- [x] **D4** — Segmentation overlays (outlines + labels on everything)
- [x] **D5** — Live stats panel (FPS, inference, CPU, confidence…)
- [x] **D6** — Detected-objects panel (live scrollable list)
- [x] **D7** — Read text (OCR) — highlights on the video + a Text panel
- [x] **D8** — Scene understanding (Claude describes the scene)
- [x] **D9** — Ask questions (chat with your camera)
- [ ] D10–D12 — coming next

**Run it** *(requires Python 3.12)*:
```bash
cd desktop
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
./run.sh
```
See **[desktop/README.md](desktop/README.md)**.

### 🌐 Web Edition (v1 — Phases 1–8, complete)
The original React + FastAPI build (detection, animated overlays, live stats, OCR).
Kept and working — see **[frontend/](frontend/)** + **[backend/](backend/)**.

---

## 📄 License

[MIT](LICENSE)
