"""The 'Assistant' chat panel — ask questions (typed or spoken) about the scene."""

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class AssistantPanel(QFrame):
    ask_requested = Signal(str)
    mic_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setProperty("panel", True)
        self._pending = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 14, 16, 16)
        outer.setSpacing(10)

        head = QHBoxLayout()
        title = QLabel("Assistant")
        title.setObjectName("PanelTitle")
        self.speaker = QPushButton("🔈")
        self.speaker.setObjectName("SpeakerToggle")
        self.speaker.setCheckable(True)
        self.speaker.setCursor(Qt.PointingHandCursor)
        self.speaker.setToolTip("Read answers aloud")
        self.speaker.setFixedSize(30, 26)
        self.speaker.toggled.connect(lambda on: self.speaker.setText("🔊" if on else "🔈"))
        head.addWidget(title)
        head.addStretch(1)
        head.addWidget(self.speaker)
        outer.addLayout(head)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        self._messages = QVBoxLayout(container)
        self._messages.setContentsMargins(0, 0, 0, 0)
        self._messages.setSpacing(8)
        self._messages.addStretch(1)
        self.scroll.setWidget(container)
        outer.addWidget(self.scroll, 1)

        self._hint = QLabel(
            "Ask me about what you see — “what's on my desk?”, “how many bottles?”, “read that label”. "
            "Tap 🎤 to speak, 🔈 to hear answers."
        )
        self._hint.setObjectName("PanelBody")
        self._hint.setWordWrap(True)
        self._messages.insertWidget(0, self._hint)

        row = QHBoxLayout()
        row.setSpacing(8)
        self.mic = QPushButton("🎤")
        self.mic.setObjectName("MicButton")
        self.mic.setCursor(Qt.PointingHandCursor)
        self.mic.setFixedSize(38, 38)
        self.mic.setToolTip("Speak your question")
        self.mic.clicked.connect(self.mic_clicked)
        self.input = QLineEdit()
        self.input.setObjectName("ChatInput")
        self.input.setPlaceholderText("Ask about what you see…")
        self.input.returnPressed.connect(self._send)
        self.send_btn = QPushButton("Ask")
        self.send_btn.setObjectName("ChatSend")
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.clicked.connect(self._send)
        row.addWidget(self.mic)
        row.addWidget(self.input, 1)
        row.addWidget(self.send_btn)
        outer.addLayout(row)

    # ── public API ──
    def speaking_enabled(self) -> bool:
        return self.speaker.isChecked()

    def submit_question(self, text: str) -> None:
        text = text.strip()
        if not text or self._pending is not None:
            return
        self._hint.hide()
        self._add_bubble(text, user=True)
        self._pending = self._add_bubble("…", user=False)
        self.input.setEnabled(False)
        self.send_btn.setEnabled(False)
        self.ask_requested.emit(text)

    def resolve(self, answer: str) -> None:
        if self._pending is not None:
            self._pending.setText(answer)
            self._pending = None
        else:
            self._add_bubble(answer, user=False)
        self.input.setEnabled(True)
        self.send_btn.setEnabled(True)
        self.input.setFocus()
        self._scroll_to_bottom()

    def add_ai(self, text: str) -> None:
        self._hint.hide()
        self._add_bubble(text, user=False)

    def set_recording(self, recording: bool) -> None:
        self.mic.setText("●" if recording else "🎤")
        self.mic.setProperty("recording", recording)
        self.mic.style().unpolish(self.mic)
        self.mic.style().polish(self.mic)
        self.input.setPlaceholderText("Listening… tap ● to stop" if recording else "Ask about what you see…")

    # ── internals ──
    def _send(self) -> None:
        text = self.input.text().strip()
        if not text:
            return
        self.input.clear()
        self.submit_question(text)

    def _add_bubble(self, text: str, user: bool) -> QLabel:
        bubble = QLabel(text)
        bubble.setObjectName("ChatUser" if user else "ChatAI")
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(250)

        wrap = QHBoxLayout()
        wrap.setContentsMargins(0, 0, 0, 0)
        if user:
            wrap.addStretch(1)
            wrap.addWidget(bubble)
        else:
            wrap.addWidget(bubble)
            wrap.addStretch(1)
        holder = QWidget()
        holder.setLayout(wrap)

        self._messages.insertWidget(self._messages.count() - 1, holder)
        self._scroll_to_bottom()
        return bubble

    def _scroll_to_bottom(self) -> None:
        bar = self.scroll.verticalScrollBar()
        QTimer.singleShot(0, lambda: bar.setValue(bar.maximum()))
