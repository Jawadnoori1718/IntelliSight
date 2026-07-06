"""Webcam capture running in a background thread.

Reading frames from a camera is blocking, so it happens on a QThread; each frame
is converted to a QImage and delivered to the UI via a Qt signal (thread-safe).
"""

import cv2
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage


def bgr_to_qimage(frame_bgr) -> QImage:
    """Convert an OpenCV BGR frame to a self-owned QImage (RGB)."""
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    height, width, channels = rgb.shape
    image = QImage(rgb.data, width, height, channels * width, QImage.Format_RGB888)
    return image.copy()  # copy so the QImage owns its pixels


class CameraWorker(QThread):
    frame_ready = Signal(QImage)   # for display
    frame_np = Signal(object)      # raw BGR frame for the vision engine
    error = Signal(str)

    def __init__(self, index: int = 0, parent=None):
        super().__init__(parent)
        self._index = index
        self._running = False

    def run(self) -> None:
        cap = cv2.VideoCapture(self._index)
        if not cap.isOpened():
            self.error.emit(
                "Could not open the camera. Make sure it's connected, not in use by "
                "another app, and that this app has camera permission "
                "(System Settings → Privacy & Security → Camera)."
            )
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self._running = True
        while self._running:
            ok, frame = cap.read()
            if not ok:
                self.msleep(15)
                continue
            self.frame_ready.emit(bgr_to_qimage(frame))
            self.frame_np.emit(frame)  # cv2 returns a fresh array each read
            self.msleep(12)  # ~ up to the camera's frame rate

        cap.release()

    def stop(self) -> None:
        self._running = False
        self.wait(2000)
