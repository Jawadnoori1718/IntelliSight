"""The Big Brother logo — a glossy camera-lens eye, drawn as vector art.

A rounded-square badge holding a realistic lens: a radial-gradient iris with
aperture blades, a deep pupil, a bright catchlight, and a rim highlight — so it
reads as a real watching lens, crisp at any size.
"""

import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QIcon,
    QLinearGradient,
    QPainter,
    QPen,
    QPixmap,
    QPolygonF,
    QRadialGradient,
)
from PySide6.QtWidgets import QWidget


def paint_mark(painter: QPainter, size: float) -> None:
    painter.setRenderHint(QPainter.Antialiasing, True)
    cx = cy = size / 2

    # ── Rounded-square badge with a diagonal gradient ──
    rect = QRectF(size * 0.03, size * 0.03, size * 0.94, size * 0.94)
    radius = size * 0.26
    badge = QLinearGradient(0, 0, size, size)
    badge.setColorAt(0.0, QColor("#0ea5e9"))
    badge.setColorAt(1.0, QColor("#4f46e5"))
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(badge))
    painter.drawRoundedRect(rect, radius, radius)

    # Soft top-left sheen on the badge
    sheen = QRadialGradient(size * 0.34, size * 0.30, size * 0.85)
    sheen.setColorAt(0.0, QColor(255, 255, 255, 70))
    sheen.setColorAt(0.55, QColor(255, 255, 255, 0))
    painter.setBrush(sheen)
    painter.drawRoundedRect(rect, radius, radius)

    # ── Lens body (dark ring) ──
    lens_r = size * 0.345
    painter.setBrush(QColor(7, 11, 22))
    painter.drawEllipse(QPointF(cx, cy), lens_r, lens_r)

    # ── Iris (radial gradient, lit from upper-left) ──
    iris_r = size * 0.285
    iris = QRadialGradient(cx - size * 0.06, cy - size * 0.06, iris_r * 1.35)
    iris.setColorAt(0.0, QColor("#a5e8ff"))
    iris.setColorAt(0.45, QColor("#38bdf8"))
    iris.setColorAt(1.0, QColor("#312e81"))
    painter.setBrush(iris)
    painter.drawEllipse(QPointF(cx, cy), iris_r, iris_r)

    # ── Aperture blades (hexagon) ──
    hexagon = [
        QPointF(cx + iris_r * 0.98 * math.cos(math.pi / 6 + k * math.pi / 3),
                cy + iris_r * 0.98 * math.sin(math.pi / 6 + k * math.pi / 3))
        for k in range(6)
    ]
    painter.setPen(QPen(QColor(255, 255, 255, 55), max(1.0, size * 0.012)))
    painter.setBrush(Qt.NoBrush)
    painter.drawPolygon(QPolygonF(hexagon))
    painter.setPen(QPen(QColor(10, 20, 45, 90), max(1.0, size * 0.01)))
    for vertex in hexagon:
        painter.drawLine(vertex, QPointF(cx, cy))

    # ── Pupil (deep, domed) ──
    pupil_r = size * 0.125
    pupil = QRadialGradient(cx - size * 0.02, cy - size * 0.02, pupil_r * 1.5)
    pupil.setColorAt(0.0, QColor("#0b1220"))
    pupil.setColorAt(1.0, QColor("#000000"))
    painter.setPen(Qt.NoPen)
    painter.setBrush(pupil)
    painter.drawEllipse(QPointF(cx, cy), pupil_r, pupil_r)

    # ── Catchlight + secondary glint ──
    painter.setBrush(QColor(255, 255, 255, 235))
    painter.drawEllipse(QPointF(cx - size * 0.055, cy - size * 0.075), size * 0.037, size * 0.052)
    painter.setBrush(QColor(255, 255, 255, 120))
    painter.drawEllipse(QPointF(cx + size * 0.055, cy + size * 0.05), size * 0.022, size * 0.022)

    # ── Lens rim highlight ──
    painter.setPen(QPen(QColor(255, 255, 255, 60), max(1.0, size * 0.011)))
    painter.setBrush(Qt.NoBrush)
    painter.drawEllipse(QPointF(cx, cy), lens_r * 0.99, lens_r * 0.99)


class BrandMark(QWidget):
    def __init__(self, size: int = 34, parent=None):
        super().__init__(parent)
        self._size = size
        self.setFixedSize(size, size)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        paint_mark(painter, self._size)
        painter.end()


def make_icon(size: int = 256) -> QIcon:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    paint_mark(painter, size)
    painter.end()
    return QIcon(pixmap)
