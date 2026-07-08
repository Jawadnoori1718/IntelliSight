"""The main window: nothing but the full-bleed camera stage.

The brand, status, detected-objects card, and Stop control all live as glass
overlays inside the camera stage itself, so the window stays out of the way and
the camera fills almost the entire screen.
"""

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .brandmark import make_icon
from .widgets.camera_stage import CameraStage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Big Brother")
        self.setWindowIcon(make_icon())
        self.resize(1280, 800)
        self.setMinimumSize(900, 600)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(10, 10, 10, 10)

        self.camera_stage = CameraStage()
        layout.addWidget(self.camera_stage)

    def closeEvent(self, event) -> None:
        self.camera_stage.shutdown()
        super().closeEvent(event)
