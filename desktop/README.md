# IntelliSight — Desktop 🖥️

A focused, **real-time object detector** — a native Mac app (PySide6) that points
your webcam at the world and cleanly boxes and names what it's sure about.

- 🎯 Accurate **YOLO11** detection on the **Apple GPU (MPS)**
- ▭ Clean rounded **bounding boxes** with category colours
- 🔒 **Locked confidence** — a box only appears once the model is sure, and its
  percentage then stays steady (no flicker)
- 📋 A simple **live list** of what's in view
- ⚡ Fully **offline & free** — no API keys, no cloud

---

## ⚠️ Requires Python 3.12

```bash
brew install python@3.12   # once, if you don't have it
```

## 🚀 Quick start

```bash
cd ~/Desktop/IntelliSight/desktop
python3.12 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
./run.sh
```

> The first run downloads PyTorch + YOLO (a few hundred MB) and the detection
> model (`yolo11l.pt`, ~50 MB). After that it starts fast.

Click **Start Camera**, and IntelliSight boxes and names objects it's confident
about, keeping a live tally on the right.

---

## 🗂️ Structure

```
desktop/
├── requirements.txt
├── run.sh
└── intellisight/
    ├── app.py            # entry point
    ├── main_window.py    # window: header, camera, objects list
    ├── theme.py          # dark neon Qt stylesheet
    ├── camera.py         # webcam capture (thread)
    ├── vision.py         # YOLO11 detector
    ├── tracker.py        # confidence-lock + box smoothing
    ├── vision_worker.py  # detection + tracking (thread)
    ├── overlay.py        # draws the boxes
    └── widgets/
        ├── camera_stage.py
        └── objects_panel.py
```
