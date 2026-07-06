# 🗺️ IntelliSight — Build Roadmap

IntelliSight is built in **20 small phases**. After each phase you get something that
**works and looks good**, then you push it to GitHub before we continue.

**How to read this:** `[x]` = done, `[ ]` = upcoming. We tick a box at the end of each phase.

---

## 🖥️ Desktop Edition — current focus

A **native desktop app** (PySide6) with super-accurate object **segmentation**
(coloured outlines around everything it sees). This is now the primary IntelliSight.
You push after each phase, exactly like before.

- [x] **D1 — Desktop app window + dark UI shell** — a real app window opens.
- [x] **D2 — Live camera in the window** — your webcam, inside the app.
- [x] **D3 — Accurate vision engine** — YOLO11 segmentation + Apple GPU (MPS), threaded worker.
- [x] **D4 — Segmentation overlays** — coloured outlines + boxes + labels on everything. *(the wow)*
- [x] **D5 — Live stats panel** — FPS, objects, people, inference, CPU.
- [ ] **D6 — Detected-objects panel** — live list with colours + confidence.
- [ ] **D7 — Read text (OCR)** — highlight text on screen + a text panel.
- [ ] **D8 — Scene understanding** — AI describes the whole scene.
- [ ] **D9 — Ask questions** — chat about what the camera sees.
- [ ] **D10 — Voice** — speak and hear answers.
- [ ] **D11 — Memory & timeline** — remember objects over time.
- [ ] **D12 — Polish & package** — final visuals + a launchable Mac app.

---

## 🌐 Web version (v1 — Phases 1–8, complete & kept)

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
