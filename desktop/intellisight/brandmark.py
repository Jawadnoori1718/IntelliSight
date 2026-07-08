"""The Big Brother logo — an all-seeing eye, drawn as vector art.

A gradient rounded-square badge holding a watchful eye (almond outline, iris ring,
and a red pupil): 'always watching', clean and crisp at any size.
"""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import QWidget


def paint_mark(painter: QPainter, size: float) -> None:
    painter.setRenderHint(QPainter.Antialiasing, True)
    cx = cy = size / 2

    # Gradient rounded-square badge
    rect = QRectF(size * 0.03, size * 0.03, size * 0.94, size * 0.94)
    gradient = QLinearGradient(0, 0, size, size)
    gradient.setColorAt(0.0, QColor("#38bdf8"))
    gradient.setColorAt(1.0, QColor("#6366f1"))
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(gradient))
    painter.drawRoundedRect(rect, size * 0.28, size * 0.28)

    # Eye almond
    ew, eh = size * 0.32, size * 0.205
    eye = QPainterPath()
    eye.moveTo(cx - ew, cy)
    eye.quadTo(cx, cy - eh, cx + ew, cy)
    eye.quadTo(cx, cy + eh, cx - ew, cy)
    pen = QPen(QColor(255, 255, 255, 240), max(1.3, size * 0.05))
    pen.setJoinStyle(Qt.RoundJoin)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)
    painter.drawPath(eye)

    # Iris ring
    iris = size * 0.135
    painter.setPen(QPen(QColor(255, 255, 255, 240), max(1.0, size * 0.033)))
    painter.drawEllipse(QPointF(cx, cy), iris, iris)

    # Pupil (watchful red) + catchlight
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor("#f5455f"))
    pupil = size * 0.062
    painter.drawEllipse(QPointF(cx, cy), pupil, pupil)
    painter.setBrush(QColor(255, 255, 255, 235))
    glint = size * 0.021
    painter.drawEllipse(QPointF(cx + size * 0.028, cy - size * 0.028), glint, glint)


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
