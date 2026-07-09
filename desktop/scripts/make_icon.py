"""Render the Big Brother logo into a macOS .iconset folder (all required sizes).

Called by scripts/make_app.sh, which then runs `iconutil` to produce a .icns.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # the desktop/ folder, so `bigbrother` imports
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QApplication

from bigbrother.brandmark import paint_mark

SPECS = [
    (16, "16x16"), (32, "16x16@2x"),
    (32, "32x32"), (64, "32x32@2x"),
    (128, "128x128"), (256, "128x128@2x"),
    (256, "256x256"), (512, "256x256@2x"),
    (512, "512x512"), (1024, "512x512@2x"),
]


def render(size: int, path: str) -> None:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    paint_mark(painter, size)
    painter.end()
    pixmap.save(path)


def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "build", "BigBrother.iconset")
    os.makedirs(out, exist_ok=True)
    app = QApplication.instance() or QApplication(sys.argv)  # noqa: F841
    for size, name in SPECS:
        render(size, os.path.join(out, f"icon_{name}.png"))
    print(f"rendered iconset → {out}")


if __name__ == "__main__":
    main()
