"""Runs Claude verification jobs off the main thread so the UI never blocks."""

import threading

from PySide6.QtCore import QThread, Signal


class ClaudeWorker(QThread):
    verify_done = Signal(object, object, str)  # firing, ok (True|False|None), reason

    def __init__(self, client, parent=None):
        super().__init__(parent)
        self._client = client
        self._jobs = []
        self._lock = threading.Lock()
        self._running = False

    def submit(self, firing, frame, question) -> None:
        with self._lock:
            self._jobs.append((firing, frame, question))

    def run(self) -> None:
        self._running = True
        while self._running:
            job = None
            with self._lock:
                if self._jobs:
                    job = self._jobs.pop(0)
            if job is None:
                self.msleep(25)
                continue
            firing, frame, question = job
            ok, reason = self._client.verify(frame, question)
            if self._running:
                self.verify_done.emit(firing, ok, reason)

    def stop(self, wait_ms=1500) -> bool:
        """Ask the loop to finish. Returns True if it's still running (a network
        call is in flight) so the caller can let it drain instead of destroying it."""
        self._running = False
        self.wait(wait_ms)
        return self.isRunning()
