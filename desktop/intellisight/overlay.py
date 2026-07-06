"""Paint segmentation outlines, masks and labels onto a video frame (QImage).

Detections carry coordinates normalised to 0..1, so we scale them by the image
size and draw straight onto the frame — the whole annotated image then scales as
one, keeping overlays perfectly aligned with the video.
"""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPen, QPolygonF

CATEGORY_COLORS = {
    "person": QColor("#38bdf8"),
    "tech": QColor("#a78bfa"),
    "food": QColor("#fb923c"),
    "furniture": QColor("#34d399"),
    "object": QColor("#94a3b8"),
}
_LABEL_TEXT = QColor("#05070e")


def _color(category: str) -> QColor:
    return CATEGORY_COLORS.get(category, CATEGORY_COLORS["object"])


def draw_detections(image: QImage, detections: list) -> QImage:
    """Draw all detections onto `image` in place and return it."""
    if not detections:
        return image

    width = image.width()
    height = image.height()

    painter = QPainter(image)
    painter.setRenderHint(QPainter.Antialiasing, True)

    font = QFont("Helvetica Neue")
    font.setPixelSize(max(13, int(height * 0.024)))
    font.setBold(True)
    painter.setFont(font)

    # Draw least-confident first so the strongest labels end up on top.
    for det in reversed(detections):
        color = _color(det["category"])
        polygon = det.get("polygon")

        if polygon and len(polygon) >= 3:
            qpoly = QPolygonF([QPointF(px * width, py * height) for px, py in polygon])

            fill = QColor(color)
            fill.setAlpha(46)
            painter.setPen(Qt.NoPen)
            painter.setBrush(fill)
            painter.drawPolygon(qpoly)

            painter.setBrush(Qt.NoBrush)
            glow = QColor(color)
            glow.setAlpha(90)
            painter.setPen(QPen(glow, 6))
            painter.drawPolygon(qpoly)

            painter.setPen(QPen(color, 2))
            painter.drawPolygon(qpoly)
        else:
            box = det["box"]
            rect = QRectF(
                box["x1"] * width,
                box["y1"] * height,
                (box["x2"] - box["x1"]) * width,
                (box["y2"] - box["y1"]) * height,
            )
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(color, 2))
            painter.drawRoundedRect(rect, 8, 8)

        _draw_label(painter, det, color, width, height)

    painter.end()
    return image


def _draw_label(painter: QPainter, det: dict, color: QColor, width: int, height: int) -> None:
    text = f"{det['label']}  {int(det['confidence'] * 100)}%"
    metrics = painter.fontMetrics()
    pad_x, pad_y = 8, 4
    rect_w = metrics.horizontalAdvance(text) + pad_x * 2
    rect_h = metrics.height() + pad_y

    box = det["box"]
    box_x = box["x1"] * width
    box_y = box["y1"] * height

    label_y = box_y - rect_h - 3
    if label_y < 0:
        label_y = box_y + 3
    label_x = max(0.0, min(box_x, width - rect_w))

    label_rect = QRectF(label_x, label_y, rect_w, rect_h)
    painter.setPen(Qt.NoPen)
    painter.setBrush(color)
    painter.drawRoundedRect(label_rect, 6, 6)

    painter.setPen(_LABEL_TEXT)
    painter.drawText(label_rect, Qt.AlignCenter, text)
