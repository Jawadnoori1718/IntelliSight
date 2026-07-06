"""Runs the segmentation engine in a background thread.

It always processes the *latest* submitted frame and drops older ones, so a slow
model never backs up the smooth camera preview.
"""

import threading

from PySide6.QtCore import QThread, Signal


class VisionWorker(QThread):
    results_ready = Signal(object)  # list[detection]
    status = Signal(str)            # loading | ready | error

    def __init__(self, parent=None):
        super().__init__(parent)
        self._engine = None
        self._latest = None
        self._lock = threading.Lock()
        self._running = False

    def submit(self, frame) -> None:
        """Hand the worker the newest frame (overwrites any unprocessed one)."""
        with self._lock:
            self._latest = frame

    def run(self) -> None:
        try:
            self.status.emit("loading")
            from .vision import SegmentationEngine

            self._engine = SegmentationEngine()
            self._engine.load()
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
                self.results_ready.emit(self._engine.infer(frame))
            except Exception:
                # A single bad frame shouldn't kill the worker.
                self.msleep(5)

    def stop(self) -> None:
        self._running = False
        self.wait(5000)
