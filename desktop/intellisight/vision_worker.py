"""Runs detection + tracking in a background thread.

Always processes the latest submitted frame (drops older ones), runs it through
the detector and the Tracker, and emits the confirmed, stable objects.
"""

import threading

from PySide6.QtCore import QThread, Signal


class VisionWorker(QThread):
    results_ready = Signal(object)  # list of confirmed, stable detections
    status = Signal(str)            # loading | ready | error

    def __init__(self, parent=None):
        super().__init__(parent)
        self._detector = None
        self._latest = None
        self._lock = threading.Lock()
        self._running = False

    def submit(self, frame) -> None:
        with self._lock:
            self._latest = frame

    def run(self) -> None:
        try:
            self.status.emit("loading")
            from .tracker import Tracker
            from .vision import Detector

            self._detector = Detector()
            self._detector.load()
            tracker = Tracker()
            self.status.emit("ready")
        except Exception:
            self.status.emit("error")
            return

        self._running = True
        while self._running:
            with self._lock:
                frame = self._latest
                self._latest = None
            if frame is None:
                self.msleep(5)
                continue
            try:
                detections = self._detector.detect(frame)
                self.results_ready.emit(tracker.update(detections))
            except Exception:
                self.msleep(5)

    def stop(self) -> None:
        self._running = False
        self.wait(5000)
