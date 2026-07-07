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

A dark, sleek IntelliSight window opens.

### 🧠 Enable AI features (optional)

Scene understanding (and later chat/voice) use **Claude**. To turn them on, add your
Anthropic API key:

```bash
cp .env.example .env        # then edit .env and paste your key
```

Get a key at **https://console.anthropic.com/**. Without a key the app runs fine —
the "Current Scene" panel just shows how to add one. Default model is `claude-opus-4-8`;
set `INTELLISIGHT_SCENE_MODEL=claude-haiku-4-5` in `.env` for a cheaper/faster option.

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
