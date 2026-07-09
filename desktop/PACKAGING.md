# Making Big Brother a Mac app 🖥️

Right now you launch it from the terminal with `./run.sh`. Here's how to turn it
into a real double-clickable Mac app.

---

## ✅ Easiest — a double-clickable app (recommended)

This wraps your existing setup in a `BigBrother.app` bundle (with the eye icon).
It's tiny and builds in seconds because it reuses your `.venv`.

```bash
cd ~/Desktop/BigBrother/desktop
./scripts/make_app.sh
```

That creates **`BigBrother.app`** right next to the code. Now you can:

- **Double-click** it to launch (no terminal window).
- Drag it into **/Applications** so it shows up in Launchpad and Spotlight.
- Drag it to your **Dock** to keep it one click away.

The first time you open it, macOS may say *"BigBrother can't be opened because it
is from an unidentified developer."* → **right-click → Open → Open**, once. And
it'll ask for **camera permission** the first time — click **Allow**.

> ⚠️ The app remembers where this folder is. If you **move or rename** the
> `Big Brother` folder, just run `./scripts/make_app.sh` again to rebuild it.

---

## 📦 Fully standalone `.app` (share it / no Python needed)

The app above still needs your `.venv` on this Mac. To make a self-contained app
that runs on a Mac **without** Python installed, freeze it with **PyInstaller**:

```bash
cd ~/Desktop/BigBrother/desktop
.venv/bin/pip install pyinstaller
.venv/bin/pyinstaller --windowed --name "Big Brother" \
  --icon build/BigBrother.icns \
  --collect-all ultralytics --collect-all torch --collect-all cv2 \
  -m bigbrother.app
```

The finished app lands in `dist/Big Brother.app`.

**Heads-up:** it will be **large** (~2–4 GB) because it bundles PyTorch and the
detection model, and the first build takes a while. This is normal for an AI app.
If PyInstaller misses a data file at runtime, add another `--collect-all <pkg>`
and rebuild. (`briefcase` and `py2app` are alternatives if you prefer.)

For sharing it with *other* people you'd also **code-sign and notarize** it with
an Apple Developer account — not needed just for yourself.

---

## Which should I use?

| Goal | Use |
|---|---|
| Just want to double-click it on **my** Mac | `./scripts/make_app.sh` ✅ |
| Give it to a friend / no Python on their Mac | PyInstaller (standalone) |
| Put it on the App Store | PyInstaller + code-sign + notarize (bigger effort) |
