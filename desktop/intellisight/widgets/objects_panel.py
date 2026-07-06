"""The 'Detected Objects' panel — a live, scrollable list of what's detected."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

CATEGORY_HEX = {
    "person": "#38bdf8",
    "tech": "#a78bfa",
    "food": "#fb923c",
    "furniture": "#34d399",
    "object": "#94a3b8",
}
MAX_ROWS = 30


class ObjectRow(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("ObjRow")
        self._color = None

        row = QHBoxLayout(self)
        row.setContentsMargins(10, 8, 10, 8)
        row.setSpacing(10)

        self.dot = QFrame()
        self.dot.setFixedSize(10, 10)

        middle = QVBoxLayout()
        middle.setSpacing(5)
        self.name = QLabel()
        self.name.setObjectName("ObjName")
        self.bar = QProgressBar()
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(5)
        self.bar.setRange(0, 100)
        middle.addWidget(self.name)
        middle.addWidget(self.bar)

        self.pct = QLabel()
        self.pct.setObjectName("ObjPct")

        row.addWidget(self.dot)
        row.addLayout(middle, 1)
        row.addWidget(self.pct)

    def update_row(self, det: dict) -> None:
        color = CATEGORY_HEX.get(det["category"], CATEGORY_HEX["object"])
        if color != self._color:
            self._color = color
            self.dot.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
            self.bar.setStyleSheet(
                "QProgressBar { background-color: rgba(255,255,255,0.08); border: none; border-radius: 2px; }"
                f"QProgressBar::chunk {{ background-color: {color}; border-radius: 2px; }}"
            )
        self.name.setText(det["label"])
        self.pct.setText(f"{int(det['confidence'] * 100)}%")
        self.bar.setValue(int(det["confidence"] * 100))


class ObjectsPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setProperty("panel", True)
        self._rows = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 14, 16, 16)
        outer.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("Detected Objects")
        title.setObjectName("PanelTitle")
        self.count_pill = QLabel("0")
        self.count_pill.setObjectName("CountPill")
        header.addWidget(title)
        header.addStretch(1)
        header.addWidget(self.count_pill)
        outer.addLayout(header)

        scroll = QScrollArea()
        scroll.setObjectName("ObjScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        self._list = QVBoxLayout(container)
        self._list.setContentsMargins(0, 0, 0, 0)
        self._list.setSpacing(8)

        self._empty = QLabel("Nothing detected yet.")
        self._empty.setObjectName("PanelBody")
        self._empty.setWordWrap(True)
        self._list.addWidget(self._empty)
        self._list.addStretch(1)

        scroll.setWidget(container)
        outer.addWidget(scroll, 1)

    def set_message(self, text: str) -> None:
        self._empty.setText(text)
        self._empty.show()
        for row in self._rows:
            row.hide()
        self.count_pill.setText("")

    def update(self, detections: list) -> None:
        count = len(detections)
        self.count_pill.setText(str(count))

        if count == 0:
            self._empty.setText("Scanning… point the camera at some objects.")
            self._empty.show()
        else:
            self._empty.hide()

        shown = detections[:MAX_ROWS]
        for i, det in enumerate(shown):
            if i >= len(self._rows):
                row = ObjectRow()
                self._list.insertWidget(self._list.count() - 1, row)  # before the stretch
                self._rows.append(row)
            self._rows[i].update_row(det)
            self._rows[i].show()

        for j in range(len(shown), len(self._rows)):
            self._rows[j].hide()
