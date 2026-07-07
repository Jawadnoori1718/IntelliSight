"""Periodically describes the scene using Claude, on a background thread.

Runs on a gentle interval (default 15s) so it stays cheap. If no API key is
configured it emits a 'no_key' status once and stops.
"""

import threading

from PySide6.QtCore import QThread, Signal

from .config import SCENE_MODEL, get_api_key, scene_interval_seconds


class SceneWorker(QThread):
    scene_ready = Signal(object)  # {description, activity, environment, lighting}
    status = Signal(str)          # no_key | thinking | ready | error

    def __init__(self, parent=None):
        super().__init__(parent)
        self._engine = None
        self._latest_frame = None
        self._latest_labels = []
        self._lock = threading.Lock()
        self._running = False

    def submit(self, frame, labels) -> None:
        with self._lock:
            self._latest_frame = frame
            self._latest_labels = list(labels)

    def run(self) -> None:
        key = get_api_key()
        if not key:
            self.status.emit("no_key")
            return

        from .scene import SceneEngine

        self._engine = SceneEngine(key, SCENE_MODEL)
        self._running = True
        interval = scene_interval_seconds()

        self._sleep(3.0)  # let a frame + some detections arrive first
        while self._running:
            with self._lock:
                frame = self._latest_frame
                labels = list(self._latest_labels)
            if frame is not None:
                self.status.emit("thinking")
                try:
                    self.scene_ready.emit(self._engine.describe(frame, labels))
                    self.status.emit("ready")
                except Exception:
                    self.status.emit("error")
            self._sleep(interval)

    def _sleep(self, seconds: float) -> None:
        for _ in range(int(seconds * 10)):
            if not self._running:
                return
            self.msleep(100)

    def stop(self) -> None:
        self._running = False
        self.wait(12000)
