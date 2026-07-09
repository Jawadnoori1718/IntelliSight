# 🗺️ Big Brother — Build Roadmap

Big Brother is built in **20 small phases**. After each phase you get something that
**works and looks good**, then you push it to GitHub before we continue.

**How to read this:** `[x]` = done, `[ ]` = upcoming. We tick a box at the end of each phase.

---

## 🖥️ Big Brother Desktop — a focused, accurate object detector

A **native Mac app** (PySide6) that does one thing well: point the camera at
anything and it cleanly boxes and names what it's sure about.

- [x] Desktop app window + dark UI shell
- [x] Live camera in the window
- [x] **Open-vocabulary** detection (YOLO-World) on the Apple GPU (MPS), threaded —
  detects the objects you name (editable `VOCABULARY` list), not just a fixed 80
- [x] Clean rounded **bounding boxes** with category colours
- [x] **Confidence lock** — a box only shows once the model is sure, then the
  percentage stays steady (tracking + box smoothing)
- [x] Simple live **objects list** of what's in view
- [x] Fully **offline & free** — no API keys, no cloud

> *Deliberately focused:* earlier experiments with segmentation outlines, OCR,
> scene descriptions, chat, voice and a stats dashboard were removed to keep the
> app fast, reliable, and simple. (They're still in the git history if ever wanted.)

## 🌐 Web version (removed)

The original browser build (`frontend/` + `backend/`) has been retired in favour
of the desktop app.

*The original browser build (React + FastAPI). Superseded by the Desktop Edition
above, but fully working and preserved.*

### Foundation

- [x] **Phase 1 — Foundation & Repo Setup**
  Repository, README, roadmap, license, `.gitignore`, and folder structure.

- [x] **Phase 2 — Backend Skeleton**
  FastAPI server, config, `/health` endpoint, virtual environment + requirements.

- [x] **Phase 3 — Frontend Shell**
  React + Vite app with the dark, glassmorphism layout (panels, dashboard, sidebar) — no camera yet.

## Seeing

- [x] **Phase 4 — Live Camera Feed**
  Browser webcam streaming live inside the app.

- [x] **Phase 5 — Object Detection Engine**
  YOLO running in the backend, streaming detections over WebSocket.

- [x] **Phase 6 — Beautiful Detection Overlays**
  Animated rounded boxes, clean labels, confidence, category colours.

- [x] **Phase 7 — Live Statistics Dashboard**
  FPS, object count, people, text blocks, scene confidence, response time.

## Reading

- [x] **Phase 8 — OCR Engine**
  EasyOCR in the backend, reading text from frames.

- [ ] **Phase 9 — OCR Overlays & Text Panel**
  Detected text highlighted on the video and listed in a panel.

## Understanding

- [ ] **Phase 10 — AI Brain Integration**
  Wire in Claude (multimodal) with config + graceful fallback.

- [ ] **Phase 11 — Scene Understanding Panel**
  Human-like descriptions of the whole scene.

- [ ] **Phase 12 — AI Explanations & Knowledge Cards**
  Click an object → rich side panel (facts vs. estimates clearly separated).

## Interacting

- [ ] **Phase 13 — Ask Questions (Text)**
  Type questions about what the camera sees; get grounded answers.

- [ ] **Phase 14 — Voice Assistant**
  Speak to it (speech-to-text) and it answers out loud (text-to-speech).

## Remembering

- [ ] **Phase 15 — Memory Mode**
  Objects logged with time + location: "Where did I leave my phone?"

- [ ] **Phase 16 — Visual Timeline & Smart Search**
  Searchable detection history with jump-to-frame.

## Reasoning

- [ ] **Phase 17 — Object Relationships**
  Spatial reasoning: "phone is right of the laptop, near the keyboard."

- [ ] **Phase 18 — AI Insights**
  Generated observations with confidence, not certainties.

## Finishing

- [ ] **Phase 19 — UI Polish**
  Animations, glassmorphism refinement, sound, responsiveness — the wow pass.

- [ ] **Phase 20 — Final Integration & Demo**
  Full end-to-end test, documentation, demo script, and packaging.

---

### The push ritual (after every phase)

1. I finish the phase and tell you exactly what changed.
2. You run the git commands I give you to push to **your** GitHub.
3. You tell me it's pushed, and we start the next phase.

That's it — 20 clean, safe milestones. 🚀
