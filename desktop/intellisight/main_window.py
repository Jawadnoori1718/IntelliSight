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

from .assistant_worker import AssistantWorker
from .widgets.assistant_panel import AssistantPanel
from .widgets.camera_stage import CameraStage
from .widgets.objects_panel import ObjectsPanel
from .widgets.scene_panel import ScenePanel
from .widgets.stats_panel import StatsPanel
from .widgets.text_panel import TextPanel

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
        self.camera_stage.stats_changed.connect(self._on_stats)
        self.camera_stage.vision_status_changed.connect(self._on_vision_status)
        self.camera_stage.text_changed.connect(self._on_text)
        self.camera_stage.ocr_status_changed.connect(self._on_ocr_status)
        self.camera_stage.scene_changed.connect(self._on_scene)
        self.camera_stage.scene_status_changed.connect(self._on_scene_status)

        self.assistant = AssistantWorker()
        self.assistant.answer_ready.connect(self._on_answer)
        self.assistant.start()

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

        self.scene_panel = ScenePanel()
        self.assistant_panel = AssistantPanel()
        self.assistant_panel.ask_requested.connect(self._on_ask)
        self.objects_panel = ObjectsPanel()
        self.text_panel = TextPanel()
        self.stats_panel = StatsPanel()

        layout.addWidget(self.scene_panel)
        layout.addWidget(self.assistant_panel, 3)
        layout.addWidget(self.objects_panel, 2)
        layout.addWidget(self.text_panel, 1)
        layout.addWidget(self.stats_panel)
        return side

    # ── vision results → sidebar ──
    def _on_detections(self, detections) -> None:
        count = len(detections)
        people = sum(1 for d in detections if d["category"] == "person")
        self.stats_panel.set("objects", str(count))
        self.stats_panel.set("people", str(people))

        if count:
            avg = round(sum(d["confidence"] for d in detections) / count * 100)
            self.stats_panel.set("confidence", f"{avg}%")
        else:
            self.stats_panel.set("confidence", "—")

        self.objects_panel.update(detections)

    def _on_stats(self, stats) -> None:
        self.stats_panel.set("fps", str(stats.get("fps", 0)))
        self.stats_panel.set("inference", f"{stats.get('inference_ms', 0)}ms")
        self.stats_panel.set("cpu", f"{stats.get('cpu', 0)}%")

    def _on_text(self, blocks) -> None:
        self.text_panel.update(blocks)

    def _on_ocr_status(self, status: str) -> None:
        if status == "loading":
            self.text_panel.set_message("Loading the text reader… (first run downloads it)")
        elif status == "ready":
            self.text_panel.set_message("Reader ready — looking for text…")
        elif status == "error":
            self.text_panel.set_message("The text reader failed to load. Check the terminal.")

    # ── chat ──
    def _on_ask(self, question: str) -> None:
        frame = self.camera_stage.last_frame
        if frame is None:
            self.assistant_panel.resolve("Turn on the camera so I can see what you're asking about.")
            return
        labels = [d["label"] for d in self.camera_stage.detections]
        self.assistant.ask(question, frame, labels)

    def _on_answer(self, text: str) -> None:
        self.assistant_panel.resolve(text)

    def _on_scene(self, data) -> None:
        self.scene_panel.set_scene(data)

    def _on_scene_status(self, status: str) -> None:
        if status == "no_key":
            self.scene_panel.set_message(
                "Add a Claude API key to enable scene understanding — copy desktop/.env.example "
                "to desktop/.env and paste your key."
            )
        elif status == "thinking":
            self.scene_panel.set_status("analysing…")
        elif status == "ready":
            self.scene_panel.set_status("live")
        elif status == "error":
            self.scene_panel.set_status("error")

    def _on_vision_status(self, status: str) -> None:
        if status == "loading":
            self.objects_panel.set_message("Loading the AI model… (first run downloads it — please wait)")
        elif status == "ready":
            self.objects_panel.set_message("AI ready — scanning…")
        elif status == "error":
            self.objects_panel.set_message("The AI model failed to load. Check the terminal for details.")

    # ── camera status → header pill ──
    def _on_camera_status(self, status: str) -> None:
        state, text = _PILL.get(status, _PILL["idle"])
        self.status_pill.setText(text)
        self.status_pill.setProperty("state", state)
        self.status_pill.style().unpolish(self.status_pill)
        self.status_pill.style().polish(self.status_pill)
        if status in ("idle", "error"):
            self.stats_panel.reset()
            self.objects_panel.set_message("Nothing detected yet.")
            self.text_panel.set_message("No text detected yet.")
            self.scene_panel.set_message("Waiting for the camera…")

    def closeEvent(self, event) -> None:
        self.camera_stage.shutdown()
        self.assistant.stop()
        super().closeEvent(event)

    @staticmethod
    def _panel_body(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("PanelBody")
        label.setWordWrap(True)
        return label
