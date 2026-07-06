# IntelliSight — Backend

The Python **FastAPI** backend. This is IntelliSight's brain and senses:

- **YOLO** — object detection ✅ *(Phase 5)*
- **EasyOCR** — text recognition *(Phase 8)*
- **Claude (multimodal)** — scene understanding, explanations, Q&A *(Phase 10)*
- **Memory** — object timeline, search, and relationships *(Phase 15+)*
- **WebSockets** — low-latency realtime detection stream ✅ *(Phase 5)*

---

## ⚠️ Requires Python 3.12

YOLO/PyTorch need Python 3.12 (the macOS system Python 3.9 is too old). Install it once:

```bash
brew install python@3.12
```

## 🚀 Quick start

### One-time setup

```bash
cd ~/Desktop/IntelliSight/backend
python3.12 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

> The first install downloads PyTorch + Ultralytics (a few hundred MB) — give it a
> few minutes. The small YOLO model (`yolov8n.pt`, ~6 MB) auto-downloads the first
> time detection runs, and the very first frame takes ~1s to warm up; after that
> each frame is ~20–30 ms.

### Run the server

```bash
./run.sh
```

Open **http://127.0.0.1:8000/health** to confirm it's alive, and
**http://127.0.0.1:8000/docs** for the interactive API.

---

## 🔌 Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness check |
| POST | `/api/detect` | Detect objects in one uploaded image (`file=@photo.jpg`) |
| WS | `/ws/detect` | Realtime stream — send JPEG frames, receive detections |

Detections come back as normalised boxes (0–1), so the frontend can scale them to
any display size:

```json
{
  "detections": [
    { "label": "Person", "category": "person", "confidence": 0.86,
      "box": { "x1": 0.06, "y1": 0.37, "x2": 0.30, "y2": 0.84 } }
  ],
  "width": 640, "height": 480, "inference_ms": 24.0
}
```

---

## 🗂️ Structure

```
backend/
├── requirements.txt
├── .env.example
├── run.sh
└── app/
    ├── main.py           # FastAPI app: CORS, routers, lifespan
    ├── config.py         # settings (env-driven, with defaults)
    ├── routers/
    │   ├── health.py     # /health
    │   └── detect.py     # /api/detect + /ws/detect
    └── services/
        └── detector.py   # YOLO wrapper (lazy-loaded model)
```

> 🚧 OCR and AI endpoints arrive in later phases — see [`../docs/ROADMAP.md`](../docs/ROADMAP.md).
