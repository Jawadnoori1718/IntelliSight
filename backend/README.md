# IntelliSight — Backend

The Python **FastAPI** backend. This is IntelliSight's brain and senses:

- **YOLO** — object detection *(Phase 5)*
- **EasyOCR** — text recognition *(Phase 8)*
- **Claude (multimodal)** — scene understanding, explanations, Q&A *(Phase 10)*
- **Memory** — object timeline, search, and relationships *(Phase 15+)*
- **WebSockets** — low-latency realtime detection stream *(Phase 5)*

---

## 🚀 Quick start

### One-time setup

From inside the `backend/` folder:

```bash
cd ~/Desktop/IntelliSight/backend
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

### Run the server

```bash
./run.sh
```

…or manually:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Then open **http://127.0.0.1:8000/health** — you should see:

```json
{ "status": "ok", "service": "IntelliSight", "version": "0.2.0", ... }
```

Interactive API docs are auto-generated at **http://127.0.0.1:8000/docs**.

---

## 🗂️ Structure

```
backend/
├── requirements.txt      # Python dependencies
├── .env.example          # copy to .env to override defaults (optional)
├── run.sh                # start the server (dev mode, auto-reload)
└── app/
    ├── main.py           # FastAPI app: CORS, routers, lifespan
    ├── config.py         # settings (env-driven, with defaults)
    └── routers/
        └── health.py     # /health endpoint
```

> 🚧 Detection, OCR and AI endpoints arrive in later phases — see [`../docs/ROADMAP.md`](../docs/ROADMAP.md).
