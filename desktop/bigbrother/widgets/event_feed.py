"""A compact translucent 'Activity' feed of appear / disappear / dwell events."""

from datetime import datetime

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

EVENT_HEX = {
    "appeared": "#34d399",     # green
    "disappeared": "#f87171",  # red
    "lingered": "#fbbf24",     # amber
    "rule": "#818cf8",         # indigo — a rule fired
}
EVENT_VERB = {
    "appeared": "appeared",
    "disappeared": "left",
    "lingered": "lingering",
}
MAX_EVENTS = 8


class _Row(QWidget):
    def __init__(self):
        super().__init__()
        self._color = None
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(9)
        self.dot = QFrame()
        self.dot.setFixedSize(8, 8)
        self.text = QLabel()
        self.text.setObjectName("EventText")
        self.time = QLabel()
        self.time.setObjectName("EventTime")
        row.addWidget(self.dot)
        row.addWidget(self.text, 1)
        row.addWidget(self.time)

    def set(self, item: dict) -> None:
        color = EVENT_HEX.get(item["type"], "#94a3b8")
        if color != self._color:
            self._color = color
            self.dot.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
        verb = EVENT_VERB.get(item["type"], "")
        self.text.setText(f"{item['label']} {verb}".strip())
        self.time.setText(item["time"])


class EventFeed(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("EventFeed")
        self.setFixedWidth(230)
        self._events = []  # newest first, of {type, label, time}
        self._rows = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(15, 12, 15, 13)
        outer.setSpacing(10)

        title = QLabel("ACTIVITY")
        title.setObjectName("EventTitle")
        outer.addWidget(title)

        self._list = QVBoxLayout()
        self._list.setContentsMargins(0, 0, 0, 0)
        self._list.setSpacing(9)
        self._empty = QLabel("Watching for events…")
        self._empty.setObjectName("EventEmpty")
        self._empty.setWordWrap(True)
        self._list.addWidget(self._empty)
        outer.addLayout(self._list)

    def clear(self) -> None:
        self._events = []
        self._empty.setText("Watching for events…")
        self._render()

    def add(self, event: dict) -> None:
        item = {
            "type": event["type"],
            "label": event["label"],
            "time": datetime.now().strftime("%I:%M:%S %p").lstrip("0"),
        }
        self._events.insert(0, item)
        self._events = self._events[:MAX_EVENTS]
        self._render()

    def _render(self) -> None:
        self._empty.setVisible(len(self._events) == 0)
        for i in range(len(self._events)):
            if i >= len(self._rows):
                row = _Row()
                self._list.addWidget(row)
                self._rows.append(row)
            self._rows[i].set(self._events[i])
            self._rows[i].show()
        for j in range(len(self._events), len(self._rows)):
            self._rows[j].hide()
