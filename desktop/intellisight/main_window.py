"""The main application window and its dark, sleek layout shell."""

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

# camera status -> (pill state property, pill text)
_PILL = {
    "idle": ("idle", "●  STANDBY"),
    "starting": ("idle", "●  CONNECTING"),
    "live": ("live", "●  LIVE"),
    "error": ("error", "●  OFFLINE"),
}


class Panel(QFrame):
    """A rounded glass-style sidebar panel with a title and a body area."""

    def __init__(self, title: str):
        super().__init__()
        self.setProperty("panel", True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 16)
        layout.setSpacing(10)

        heading = QLabel(title)
        heading.setObjectName("PanelTitle")
        layout.addWidget(heading)

        self.body = layout


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
        subtitle = QLabel("VISUAL INTELLIGENCE")
        subtitle.setObjectName("BrandSub")
        brand.addWidget(title)
        brand.addWidget(subtitle)
        layout.addLayout(brand)

        layout.addStretch(1)

        self.status_pill = QLabel("●  STANDBY")
        self.status_pill.setObjectName("StatusPill")
        layout.addWidget(self.status_pill)

        return header

    # ── Sidebar ──
    def _build_sidebar(self) -> QWidget:
        side = QWidget()
        side.setFixedWidth(360)

        layout = QVBoxLayout(side)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        scene = Panel("Current Scene")
        self.scene_body = self._panel_body("Waiting for the camera…")
        scene.body.addWidget(self.scene_body)

        objects = Panel("Detected Objects")
        self.objects_body = self._panel_body("Nothing detected yet.")
        objects.body.addWidget(self.objects_body)

        stats = Panel("Live Stats")
        self.stats_body = self._panel_body("Start the camera to see live stats.")
        stats.body.addWidget(self.stats_body)

        layout.addWidget(scene)
        layout.addWidget(objects)
        layout.addWidget(stats, 1)
        return side

    # ── vision results → sidebar ──
    def _on_detections(self, detections) -> None:
        if not detections:
            self.objects_body.setText("Scanning… point the camera at some objects.")
            return
        seen = []
        for det in detections:
            if det["label"] not in seen:
                seen.append(det["label"])
        self.objects_body.setText(f"{len(detections)} detected — " + ", ".join(seen[:10]))

    def _on_vision_status(self, status: str) -> None:
        if status == "loading":
            self.objects_body.setText("Loading the AI model… (first run downloads it — please wait)")
        elif status == "ready":
            self.objects_body.setText("AI ready — scanning…")
        elif status == "error":
            self.objects_body.setText("The AI model failed to load. Check the terminal for details.")

    # ── camera status → header pill ──
    def _on_camera_status(self, status: str) -> None:
        state, text = _PILL.get(status, _PILL["idle"])
        self.status_pill.setText(text)
        self.status_pill.setProperty("state", state)
        self.status_pill.style().unpolish(self.status_pill)
        self.status_pill.style().polish(self.status_pill)

    def closeEvent(self, event) -> None:
        self.camera_stage.shutdown()
        super().closeEvent(event)

    @staticmethod
    def _panel_body(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("PanelBody")
        label.setWordWrap(True)
        return label
