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
        body.addWidget(self._build_stage(), 1)
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

    # ── Camera stage ──
    def _build_stage(self) -> QFrame:
        stage = QFrame()
        stage.setObjectName("Stage")

        layout = QVBoxLayout(stage)
        layout.addStretch(1)

        icon = QLabel("📷")
        icon.setObjectName("StageIcon")
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        title = QLabel("Camera feed appears here")
        title.setObjectName("StageTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        hint = QLabel("Live webcam arrives in Phase D2.")
        hint.setObjectName("StageHint")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        layout.addStretch(1)
        return stage

    # ── Sidebar ──
    def _build_sidebar(self) -> QWidget:
        side = QWidget()
        side.setFixedWidth(360)

        layout = QVBoxLayout(side)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        scene = Panel("Current Scene")
        scene.body.addWidget(self._panel_body("Waiting for the camera…"))

        objects = Panel("Detected Objects")
        objects.body.addWidget(self._panel_body("Nothing detected yet."))

        stats = Panel("Live Stats")
        stats.body.addWidget(self._panel_body("Start the camera to see live stats."))

        layout.addWidget(scene)
        layout.addWidget(objects)
        layout.addWidget(stats, 1)
        return side

    @staticmethod
    def _panel_body(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("PanelBody")
        label.setWordWrap(True)
        return label
