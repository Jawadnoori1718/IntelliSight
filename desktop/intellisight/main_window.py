"""The main application window: header, camera stage, and a live objects list."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from .widgets.camera_stage import CameraStage
from .widgets.objects_panel import ObjectsPanel

# camera status -> (pill state property, pill text)
_PILL = {
    "idle": ("idle", "●  STANDBY"),
    "starting": ("idle", "●  CONNECTING"),
    "live": ("live", "●  LIVE"),
    "error": ("error", "●  OFFLINE"),
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IntelliSight")
        self.resize(1320, 820)
        self.setMinimumSize(980, 640)

        root = QWidget()
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(16)

        outer.addWidget(self._build_header())

        body = QHBoxLayout()
        body.setSpacing(16)
        self.camera_stage = CameraStage()
        self.camera_stage.status_changed.connect(self._on_camera_status)
        self.camera_stage.detections_changed.connect(self._on_detections)
        self.camera_stage.vision_status_changed.connect(self._on_vision_status)
        body.addWidget(self.camera_stage, 1)
        body.addWidget(self._build_sidebar())
        outer.addLayout(body, 1)

    # ── Header ──
    def _build_header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("Header")
        header.setFixedHeight(68)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(18, 10, 18, 10)
        layout.setSpacing(14)

        badge = QLabel("👁")
        badge.setObjectName("BrandBadge")
        badge.setFixedSize(42, 42)
        badge.setAlignment(Qt.AlignCenter)
        layout.addWidget(badge)

        brand = QVBoxLayout()
        brand.setSpacing(0)
        title = QLabel("IntelliSight")
        title.setObjectName("BrandTitle")
        subtitle = QLabel("OBJECT DETECTION")
        subtitle.setObjectName("BrandSub")
        brand.addWidget(title)
        brand.addWidget(subtitle)
        layout.addLayout(brand)

        layout.addStretch(1)

        self.status_pill = QLabel("●  STANDBY")
        self.status_pill.setObjectName("StatusPill")
        layout.addWidget(self.status_pill)

        return header

    # ── Sidebar (just the detected-objects list) ──
    def _build_sidebar(self) -> QWidget:
        side = QWidget()
        side.setFixedWidth(360)
        layout = QVBoxLayout(side)
        layout.setContentsMargins(0, 0, 0, 0)
        self.objects_panel = ObjectsPanel()
        layout.addWidget(self.objects_panel)
        return side

    # ── slots ──
    def _on_detections(self, detections) -> None:
        self.objects_panel.update(detections)

    def _on_vision_status(self, status: str) -> None:
        if status == "loading":
            self.objects_panel.set_message("Loading the detector… (first run downloads it — please wait)")
        elif status == "ready":
            self.objects_panel.set_message("Ready — scanning…")
        elif status == "error":
            self.objects_panel.set_message("The detector failed to load. Check the terminal for details.")

    def _on_camera_status(self, status: str) -> None:
        state, text = _PILL.get(status, _PILL["idle"])
        self.status_pill.setText(text)
        self.status_pill.setProperty("state", state)
        self.status_pill.style().unpolish(self.status_pill)
        self.status_pill.style().polish(self.status_pill)
        if status in ("idle", "error"):
            self.objects_panel.set_message("Nothing detected yet.")

    def closeEvent(self, event) -> None:
        self.camera_stage.shutdown()
        super().closeEvent(event)
