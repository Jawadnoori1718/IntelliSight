"""Answers chat questions on a background thread (one at a time, in order)."""

import threading

from PySide6.QtCore import QThread, Signal

from .config import SCENE_MODEL, get_api_key

_NO_KEY = (
    "Add a Claude API key to chat — copy desktop/.env.example to desktop/.env "
    "and paste your key."
)
_ERROR = "Sorry — I couldn't reach the AI. Check your API key and internet connection."


class AssistantWorker(QThread):
    answer_ready = Signal(str)  # success or a friendly error message

    def __init__(self, parent=None):
        super().__init__(parent)
        self._engine = None
        self._queue = []
        self._lock = threading.Lock()
        self._event = threading.Event()
        self._running = False

    def ask(self, question: str, frame, labels) -> None:
        with self._lock:
            self._queue.append((question, frame, list(labels)))
        self._event.set()

    def run(self) -> None:
        key = get_api_key()
        if key:
            from .assistant import AssistantEngine

            self._engine = AssistantEngine(key, SCENE_MODEL)

        self._running = True
        while self._running:
            self._event.wait()
            if not self._running:
                break
            while True:
                with self._lock:
                    if not self._queue:
                        self._event.clear()
                        break
                    question, frame, labels = self._queue.pop(0)
                if self._engine is None:
                    self.answer_ready.emit(_NO_KEY)
                    continue
                try:
                    self.answer_ready.emit(self._engine.answer(question, frame, labels))
                except Exception:
                    self.answer_ready.emit(_ERROR)

    def stop(self) -> None:
        self._running = False
        self._event.set()
        self.wait(12000)
