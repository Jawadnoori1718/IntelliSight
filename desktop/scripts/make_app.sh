#!/usr/bin/env bash
# Build BigBrother.app — a double-clickable Mac app that launches Big Brother.
#
# It wraps your existing virtualenv, so it's small and fast to build. Run it once
# (re-run after moving the folder or changing the icon):
#     ./scripts/make_app.sh
set -e

HERE="$(cd "$(dirname "$0")/.." && pwd)"   # the desktop/ folder
APP="$HERE/BigBrother.app"
VENV="$HERE/.venv"
BUILD="$HERE/build"

if [ ! -x "$VENV/bin/python" ]; then
  echo "❌  No virtualenv at $VENV — run the setup in README.md first."
  exit 1
fi

echo "🎨  Rendering app icon…"
mkdir -p "$BUILD"
ICONSET="$BUILD/BigBrother.iconset"
rm -rf "$ICONSET"; mkdir -p "$ICONSET"
"$VENV/bin/python" "$HERE/scripts/make_icon.py" "$ICONSET" >/dev/null
iconutil -c icns "$ICONSET" -o "$BUILD/BigBrother.icns"

echo "📦  Building app bundle…"
rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$BUILD/BigBrother.icns" "$APP/Contents/Resources/BigBrother.icns"

cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>Big Brother</string>
  <key>CFBundleDisplayName</key><string>Big Brother</string>
  <key>CFBundleIdentifier</key><string>com.bigbrother.desktop</string>
  <key>CFBundleVersion</key><string>3.0.0</string>
  <key>CFBundleShortVersionString</key><string>3.0.0</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>BigBrother</string>
  <key>CFBundleIconFile</key><string>BigBrother</string>
  <key>NSHighResolutionCapable</key><true/>
  <key>LSMinimumSystemVersion</key><string>11.0</string>
  <key>NSCameraUsageDescription</key><string>Big Brother uses your camera to detect objects in real time.</string>
</dict>
</plist>
PLIST

# Launcher — hard-codes this machine's paths (rebuild if you move the folder).
cat > "$APP/Contents/MacOS/BigBrother" <<LAUNCH
#!/usr/bin/env bash
cd "$HERE"
exec "$VENV/bin/python" -m bigbrother.app
LAUNCH
chmod +x "$APP/Contents/MacOS/BigBrother"

# Refresh the icon cache so Finder shows the new icon immediately.
touch "$APP"

echo "✅  Built $APP"
echo "    Double-click it, or drag it into /Applications or your Dock."
