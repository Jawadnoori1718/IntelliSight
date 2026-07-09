# Big Brother — Desktop 👁️

**Always watching.** A native Mac app (PySide6) that turns your webcam into a
real-time watcher — it cleanly boxes and names what it sees, and (as it grows)
lets your space *react* to what happens in it.

- 👁️ **Open-vocabulary** detection (**YOLO-World**) on the **Apple GPU (MPS)** —
  it finds the objects *you* name (pen, keys, headphones, mug…), not a fixed list of 80
- ▭ Clean rounded **bounding boxes** with category colours
- 🔒 **Locked confidence** — a box only appears once the model is sure, and its
  percentage then stays steady (no flicker)
- 🖥️ **Camera-first UI** — the video fills the screen; a floating glass card lists
  what's in view
- ⚡ Fully **offline & free** for detection — no API keys, no cloud

> **A programmable-perception platform:** draw zones and count things, set rules like
> *"when the camera sees X, do Y"*, get desktop/phone notifications, fire webhooks
> (Home Assistant / Slack / MQTT), keep a searchable 30-day timeline, and gate any rule
> behind a plain-English **Claude** condition verified on the live frame.

---

## ⚠️ Requires Python 3.12

```bash
brew install python@3.12   # once, if you don't have it
```

## 🚀 Quick start

```bash
cd ~/Desktop/BigBrother/desktop
python3.12 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
./run.sh
```

> The first run downloads PyTorch + YOLO-World (a few hundred MB). After that it
> starts fast.

Click **Start Camera**, and Big Brother boxes and names objects it's confident
about, listing them in the floating card.

### ✏️ Add your own objects

Open **`bigbrother/vision.py`** and edit the **`VOCABULARY`** list — add any word
(e.g. `"stethoscope"`, `"rubik's cube"`, `"guitar"`) and it'll start looking for it.
No retraining needed.

---

## 🗂️ Structure

```
desktop/
├── requirements.txt
├── run.sh
└── bigbrother/
    ├── app.py            # entry point
    ├── main_window.py    # full-bleed camera window
    ├── brandmark.py      # the all-seeing-eye logo (vector)
    ├── theme.py          # dark, camera-first Qt stylesheet
    ├── camera.py         # webcam capture (thread)
    ├── vision.py         # YOLO-World open-vocabulary detector
    ├── tracker.py        # confidence-lock + box smoothing
    ├── vision_worker.py  # detection + tracking (thread)
    ├── overlay.py        # draws the boxes
    └── widgets/
        ├── camera_stage.py     # video + floating glass overlays
        └── objects_overlay.py  # the "Detected" card
```
