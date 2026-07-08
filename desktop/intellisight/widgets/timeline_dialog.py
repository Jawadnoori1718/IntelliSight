"""A searchable window over Big Brother's memory (the SQLite timeline)."""

import subprocess
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .event_feed import EVENT_HEX, EVENT_VERB


def _format_time(ts: float) -> str:
    dt = datetime.fromtimestamp(ts)
    today = datetime.now().date()
    delta = (today - dt.date()).days
    if delta == 0:
        day = "Today"
    elif delta == 1:
        day = "Yesterday"
    else:
        day = dt.strftime("%b %d")
    return f"{day}, {dt.strftime('%I:%M:%S %p').lstrip('0')}"


class TimelineDialog(QDialog):
    def __init__(self, timeline, parent=None):
        super().__init__(parent)
        self.timeline = timeline
        self.setObjectName("TimelineDialog")
        self.setWindowTitle("Timeline")
        self.setModal(True)
        self.setMinimumSize(560, 580)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 22, 24, 22)
        root.setSpacing(14)

        header = QLabel("Timeline")
        header.setObjectName("RulesHeader")
        subtitle = QLabel("Everything Big Brother has seen — kept for 30 days.")
        subtitle.setObjectName("RulesSub")
        root.addWidget(header)
        root.addWidget(subtitle)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search…  (e.g. person, keys, package)")
        self.search.textChanged.connect(self._reload)
        root.addWidget(self.search)

        self._list = QVBoxLayout()
        self._list.setContentsMargins(0, 0, 0, 0)
        self._list.setSpacing(8)
        container = QWidget()
        container.setLayout(self._list)
        container.setStyleSheet("background: transparent;")
        scroll = QScrollArea()
        scroll.setObjectName("RulesScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(container)
        scroll.viewport().setStyleSheet("background: transparent;")
        root.addWidget(scroll, 1)

        footer = QHBoxLayout()
        self.count_label = QLabel("")
        self.count_label.setObjectName("SettingsHelp")
        clear_btn = QPushButton("Clear history")
        clear_btn.setObjectName("SmallBtn")
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.clicked.connect(self._clear)
        footer.addWidget(self.count_label)
        footer.addStretch(1)
        footer.addWidget(clear_btn)
        root.addLayout(footer)

        self._reload()

    def _clear_list(self) -> None:
        while self._list.count():
            item = self._list.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _reload(self) -> None:
        self._clear_list()
        rows = self.timeline.query(self.search.text())
        if not rows:
            empty = QLabel("Nothing here yet." if not self.search.text().strip()
                           else "No matches.")
            empty.setObjectName("RulesEmpty")
            self._list.addWidget(empty)
            self._list.addStretch(1)
        else:
            for row in rows:
                self._list.addWidget(self._row(row))
            self._list.addStretch(1)
        total = self.timeline.count()
        self.count_label.setText(f"{total} event{'s' if total != 1 else ''} remembered")

    def _row(self, item: dict) -> QFrame:
        frame = QFrame()
        frame.setObjectName("RuleItem")
        row = QHBoxLayout(frame)
        row.setContentsMargins(12, 8, 12, 8)
        row.setSpacing(10)

        dot = QFrame()
        dot.setFixedSize(8, 8)
        color = EVENT_HEX.get(item["kind"], "#94a3b8")
        dot.setStyleSheet(f"background-color: {color}; border-radius: 4px;")

        verb = EVENT_VERB.get(item["kind"], "")
        prefix = "⚡ " if item["kind"] == "rule" else ""
        text = QLabel(f"{prefix}{item['label']} {verb}".strip())
        text.setObjectName("RuleDesc")

        when = QLabel(_format_time(item["ts"]))
        when.setObjectName("EventTime")

        row.addWidget(dot)
        row.addWidget(text, 1)
        row.addWidget(when)

        if item.get("snapshot"):
            view = QPushButton("View")
            view.setObjectName("SmallBtn")
            view.setCursor(Qt.PointingHandCursor)
            view.clicked.connect(lambda _=False, p=item["snapshot"]: self._open(p))
            row.addWidget(view)

        return frame

    def _open(self, path) -> None:
        try:
            subprocess.Popen(["open", path])
        except Exception:
            pass

    def _clear(self) -> None:
        self.timeline.clear()
        self._reload()
