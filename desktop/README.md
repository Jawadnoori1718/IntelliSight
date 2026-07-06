# IntelliSight — Desktop Edition 🖥️

A **native desktop application** (built with **PySide6 / Qt**) that turns your webcam
into a real-time visual-intelligence assistant — accurate object **segmentation**
(outlines around everything it sees), text reading, scene understanding and more.

This is the primary IntelliSight experience. (The `../frontend` + `../backend` web
version is kept as v1.)

---

## ⚠️ Requires Python 3.12

```bash
brew install python@3.12   # once, if you don't have it
```

## 🚀 Quick start

### One-time setup

```bash
cd ~/Desktop/IntelliSight/desktop
python3.12 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

### Run the app

```bash
./run.sh
```

A dark, sleek IntelliSight window opens. (Live camera arrives in Phase D2; accurate
object outlines in Phase D4.)

---

## 🗂️ Structure

```
desktop/
├── requirements.txt
├── run.sh
└── intellisight/
    ├── app.py            # entry point (QApplication + window)
    ├── main_window.py    # window + layout shell
    └── theme.py          # dark neon Qt stylesheet
```

> 🚧 See [`../docs/ROADMAP.md`](../docs/ROADMAP.md) → *Desktop Edition* for the plan.
