"""A compact translucent 'Detected Objects' card that floats over the video."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

CATEGORY_HEX = {
    "person": "#38bdf8",
    "tech": "#a78bfa",
    "food": "#fb923c",
    "furniture": "#34d399",
    "object": "#94a3b8",
}
MAX_ROWS = 8


class _Row(QWidget):
    def __init__(self):
        super().__init__()
        self._color = None
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(9)
        self.dot = QFrame()
        self.dot.setFixedSize(8, 8)
        self.name = QLabel()
        self.name.setObjectName("ObjRowName")
        self.pct = QLabel()
        self.pct.setObjectName("ObjRowPct")
        row.addWidget(self.dot)
        row.addWidget(self.name, 1)
        row.addWidget(self.pct)

    def set(self, det: dict) -> None:
        color = CATEGORY_HEX.get(det["category"], CATEGORY_HEX["object"])
        if color != self._color:
            self._color = color
            self.dot.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
        self.name.setText(det["label"])
        self.pct.setText(f"{int(det['confidence'] * 100)}%")


class ObjectsOverlay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ObjOverlay")
        self.setFixedWidth(236)
        self._rows = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(15, 12, 15, 13)
        outer.setSpacing(10)

        header = QHBoxLayout()
        title = QLabel("DETECTED")
        title.setObjectName("ObjTitle")
        self.count = QLabel("0")
        self.count.setObjectName("ObjCount")
        header.addWidget(title)
        header.addStretch(1)
        header.addWidget(self.count)
        outer.addLayout(header)

        self._list = QVBoxLayout()
        self._list.setContentsMargins(0, 0, 0, 0)
        self._list.setSpacing(9)
        self._empty = QLabel("Scanning…")
        self._empty.setObjectName("ObjEmpty")
        self._empty.setWordWrap(True)
        self._list.addWidget(self._empty)
        outer.addLayout(self._list)

    def set_message(self, text: str) -> None:
        self._empty.setText(text)
        self._empty.show()
        for row in self._rows:
            row.hide()
        self.count.setText("")

    def update(self, detections: list) -> None:
        self.count.setText(str(len(detections)))
        shown = detections[:MAX_ROWS]
        self._empty.setVisible(len(shown) == 0)
        if not shown:
            self._empty.setText("Scanning…")

        for i, det in enumerate(shown):
            if i >= len(self._rows):
                row = _Row()
                self._list.addWidget(row)
                self._rows.append(row)
            self._rows[i].set(det)
            self._rows[i].show()

        for j in range(len(shown), len(self._rows)):
            self._rows[j].hide()
