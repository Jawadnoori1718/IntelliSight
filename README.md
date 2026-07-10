# Big Brother

### Always watching. A native Mac app that turns your webcam into a programmable eye.

Big Brother watches a space in real time, understands what's happening, and **acts on it** —
so your camera stops being a passive feed and starts *doing things*.

---

## ✨ What it does

Point it at a room and it detects and names what it sees (open-vocabulary, so it finds the
things *you* care about — not a fixed list). Then you give it **rules**:

> **When** the camera sees a `person` **in** `[a zone you draw]` → **notify my phone**
> **When** a `package` **appears** **· only if** *Claude confirms it's a delivery* → **save a snapshot**

- 👁️ **Real-time detection** (YOLO-World) on the Apple GPU, with locked, flicker-free labels
- ▭ **Zones & counting** — draw a region, live-count what's inside
- 🔔 **Events** — appeared / left / lingering, in a live activity feed
- 🧠 **Rules engine** — *"when the camera sees X, do Y"* (alert, sound, snapshot, notify, webhook)
- 📱 **Notifications** — native macOS + your phone (via free [ntfy](https://ntfy.sh))
- 🕓 **Timeline** — a searchable 30-day memory of everything it saw
- 🔌 **Webhooks** — feed Home Assistant / Slack / MQTT / your own scripts
- 🤖 **Claude verification** *(optional)* — gate a rule behind a plain-English condition that
  Claude confirms on the live frame, for judgment the detector alone can't make

Detection runs **fully offline and free**. Claude is optional and only used if you add a key.

---

## 🚀 Run it

Requires **Python 3.12**.

```bash
cd desktop
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
./run.sh
```

Or make it a **double-clickable Mac app**:

```bash
cd desktop
./scripts/make_app.sh      # builds BigBrother.app with the lens icon
```

See **[desktop/README.md](desktop/README.md)** to run it and **[desktop/PACKAGING.md](desktop/PACKAGING.md)** to package it.

---

## 🛠️ How it works

```
  Webcam ──► YOLO-World detector ──► tracker (locks confidence, smooths boxes)
                                         │
                     events (appear/leave/linger) + zones/counts
                                         │
                                    Rules engine
                          ┌──────────────┼───────────────┐
                     local trigger   Claude verify    actions:
                     (free, instant)  (optional,      alert · sound · snapshot
                                       on the frame)   notify · webhook
                                         │
                              SQLite timeline (searchable memory)
```

- **Desktop app:** PySide6 / Qt (camera-first UI, QPainter overlays)
- **Detection:** Ultralytics **YOLO-World** (open-vocabulary), Apple **MPS** accelerated
- **Smart layer:** **Claude** vision (multimodal) — optional, rate-limited
- **Memory:** local **SQLite**

---

## 📄 License

[MIT](LICENSE)
