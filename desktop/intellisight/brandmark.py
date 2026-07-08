"""The IntelliSight logo — a minimal 'focus reticle' mark, drawn as vector art.

A gradient rounded-square badge with white camera-focus corner brackets around a
central dot: sight + detection, clean and futuristic at any size.
"""

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
)
from PySide6.QtWidgets import QWidget


def paint_mark(painter: QPainter, size: float) -> None:
    painter.setRenderHint(QPainter.Antialiasing, True)

    # Gradient rounded-square badge
    rect = QRectF(size * 0.03, size * 0.03, size * 0.94, size * 0.94)
    gradient = QLinearGradient(0, 0, size, size)
    gradient.setColorAt(0.0, QColor("#38bdf8"))
    gradient.setColorAt(1.0, QColor("#6366f1"))
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(gradient))
    painter.drawRoundedRect(rect, size * 0.28, size * 0.28)

    # White focus brackets
    inset = size * 0.28
    arm = size * 0.15
    x0, y0, x1, y1 = inset, inset, size - inset, size - inset
    pen = QPen(QColor(255, 255, 255, 235), max(1.4, size * 0.06))
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)
    painter.drawPolyline(QPolygonF([QPointF(x0, y0 + arm), QPointF(x0, y0), QPointF(x0 + arm, y0)]))
    painter.drawPolyline(QPolygonF([QPointF(x1 - arm, y0), QPointF(x1, y0), QPointF(x1, y0 + arm)]))
    painter.drawPolyline(QPolygonF([QPointF(x0, y1 - arm), QPointF(x0, y1), QPointF(x0 + arm, y1)]))
    painter.drawPolyline(QPolygonF([QPointF(x1 - arm, y1), QPointF(x1, y1), QPointF(x1, y1 - arm)]))

    # Centre dot
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor(255, 255, 255, 240))
    dot = size * 0.085
    painter.drawEllipse(QPointF(size / 2, size / 2), dot, dot)


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
