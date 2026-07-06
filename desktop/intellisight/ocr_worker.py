"""Runs OCR in a background thread at a gentle ~1×/second cadence.

OCR is much slower than object detection (~0.7s per frame), so it runs on its own
thread and pauses briefly between reads to stay light on the CPU.
"""

import threading

from PySide6.QtCore import QThread, Signal

PAUSE_MS = 400  # short rest between reads → roughly one read per second


class OCRWorker(QThread):
    ocr_ready = Signal(object)  # list[text block]
    status = Signal(str)        # loading | ready | error

    def __init__(self, parent=None):
        super().__init__(parent)
        self._engine = None
        self._latest = None
        self._lock = threading.Lock()
        self._running = False

    def submit(self, frame) -> None:
        with self._lock:
            self._latest = frame

    def run(self) -> None:
        try:
            self.status.emit("loading")
            from .ocr import OCREngine

            self._engine = OCREngine()
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
                self.msleep(50)
                continue
            try:
                self.ocr_ready.emit(self._engine.read(frame))
            except Exception:
                pass
            self.msleep(PAUSE_MS)

    def stop(self) -> None:
        self._running = False
        self.wait(6000)
