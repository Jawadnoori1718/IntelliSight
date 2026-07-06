"""The 'Text' panel — a live, scrollable list of text IntelliSight is reading."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

MAX_LINES = 20


class TextPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setProperty("panel", True)
        self._lines = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 14, 16, 16)
        outer.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("Text")
        title.setObjectName("PanelTitle")
        self.count_pill = QLabel("0")
        self.count_pill.setObjectName("CountPill")
        header.addWidget(title)
        header.addStretch(1)
        header.addWidget(self.count_pill)
        outer.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        self._list = QVBoxLayout(container)
        self._list.setContentsMargins(0, 0, 0, 0)
        self._list.setSpacing(7)

        self._empty = QLabel("No text in view — point at a book, screen or label.")
        self._empty.setObjectName("PanelBody")
        self._empty.setWordWrap(True)
        self._list.addWidget(self._empty)
        self._list.addStretch(1)

        scroll.setWidget(container)
        outer.addWidget(scroll, 1)

    def set_message(self, text: str) -> None:
        self._empty.setText(text)
        self._empty.show()
        for line in self._lines:
            line.hide()
        self.count_pill.setText("")

    def update(self, blocks: list) -> None:
        count = len(blocks)
        self.count_pill.setText(str(count))

        if count == 0:
            self._empty.setText("No text in view — point at a book, screen or label.")
            self._empty.show()
        else:
            self._empty.hide()

        shown = blocks[:MAX_LINES]
        for i, block in enumerate(shown):
            if i >= len(self._lines):
                line = QLabel()
                line.setObjectName("TextLine")
                line.setWordWrap(True)
                self._list.insertWidget(self._list.count() - 1, line)
                self._lines.append(line)
            self._lines[i].setText("“" + block["text"] + "”")
            self._lines[i].show()

        for j in range(len(shown), len(self._lines)):
            self._lines[j].hide()
