"""The camera stage: shows a start prompt, the live video, or an error state."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..camera import CameraWorker
from ..ocr_worker import OCRWorker
from ..overlay import draw_detections, draw_text_blocks
from ..scene_worker import SceneWorker
from ..vision_worker import VisionWorker


class CameraStage(QFrame):
    """Owns the camera + vision + OCR + scene workers and swaps between idle / live / error pages."""

    status_changed = Signal(str)        # idle | starting | live | error
    detections_changed = Signal(object)  # list[detection]
    stats_changed = Signal(object)       # {inference_ms, fps, cpu}
    vision_status_changed = Signal(str)  # loading | ready | error
    text_changed = Signal(object)        # list[text block]
    ocr_status_changed = Signal(str)     # loading | ready | error
    scene_changed = Signal(object)       # {description, activity, ...}
    scene_status_changed = Signal(str)   # no_key | thinking | ready | error

    def __init__(self):
        super().__init__()
        self.setObjectName("Stage")
        self.worker = None
        self.vision = None
        self.ocr = None
        self.scene = None
        self.detections = []
        self.text_blocks = []
        self.last_frame = None  # latest raw BGR frame, for the assistant
        self._got_frame = False

        self.stack = QStackedWidget()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(10, 10, 10, 10)
        outer.addWidget(self.stack)

        self.stack.addWidget(self._build_idle())   # index 0
        self.stack.addWidget(self._build_live())   # index 1
        self.stack.addWidget(self._build_error())  # index 2
        self.stack.setCurrentIndex(0)

    # ── pages ──
    def _build_idle(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.addStretch(1)
        lay.addWidget(self._center(QLabel("📷"), "StageIcon"))
        lay.addWidget(self._center(QLabel("Camera feed appears here"), "StageTitle"))
        lay.addWidget(self._center(QLabel("Turn on your webcam to bring IntelliSight to life."), "StageHint"))
        lay.addSpacing(16)
        start = QPushButton("  Start Camera")
        start.setObjectName("StartBtn")
        start.setCursor(Qt.PointingHandCursor)
        start.clicked.connect(self.start_camera)
        lay.addLayout(self._button_row(start))
        lay.addStretch(1)
        return page

    def _build_live(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        self.video_label = QLabel()
        self.video_label.setObjectName("VideoLabel")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setMinimumSize(1, 1)
        lay.addWidget(self.video_label, 1)

        stop = QPushButton("■  Stop")
        stop.setObjectName("StopBtn")
        stop.setCursor(Qt.PointingHandCursor)
        stop.clicked.connect(self.stop_camera)
        lay.addLayout(self._button_row(stop))
        return page

    def _build_error(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.addStretch(1)
        lay.addWidget(self._center(QLabel("⚠️"), "StageIcon"))
        lay.addWidget(self._center(QLabel("Couldn't start the camera"), "StageTitle"))
        self.error_label = QLabel("")
        self.error_label.setObjectName("ErrorText")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        lay.addWidget(self.error_label)
        lay.addSpacing(16)
        retry = QPushButton("  Try Again")
        retry.setObjectName("StartBtn")
        retry.setCursor(Qt.PointingHandCursor)
        retry.clicked.connect(self.start_camera)
        lay.addLayout(self._button_row(retry))
        lay.addStretch(1)
        return page

    # ── controls ──
    def start_camera(self) -> None:
        if self.worker is not None:
            return
        self._got_frame = False
        self.detections = []
        self.text_blocks = []
        self.status_changed.emit("starting")
        self.stack.setCurrentIndex(1)

        self.worker = CameraWorker(0)
        self.worker.frame_ready.connect(self._on_frame)
        self.worker.frame_np.connect(self._on_frame_np)
        self.worker.error.connect(self._on_error)

        self.vision = VisionWorker()
        self.vision.results_ready.connect(self._on_results)
        self.vision.stats_ready.connect(self.stats_changed)
        self.vision.status.connect(self.vision_status_changed)

        self.ocr = OCRWorker()
        self.ocr.ocr_ready.connect(self._on_ocr)
        self.ocr.status.connect(self.ocr_status_changed)

        self.scene = SceneWorker()
        self.scene.scene_ready.connect(self.scene_changed)
        self.scene.status.connect(self.scene_status_changed)

        self.worker.start()
        self.vision.start()
        self.ocr.start()
        self.scene.start()

    def stop_camera(self) -> None:
        self._stop_workers()
        self.stack.setCurrentIndex(0)
        self.status_changed.emit("idle")

    def shutdown(self) -> None:
        self._stop_workers()

    def _stop_workers(self) -> None:
        if self.worker is not None:
            self.worker.stop()
            self.worker = None
        if self.vision is not None:
            self.vision.stop()
            self.vision = None
        if self.ocr is not None:
            self.ocr.stop()
            self.ocr = None
        if self.scene is not None:
            self.scene.stop()
            self.scene = None
        self.text_blocks = []
        self.last_frame = None

    # ── slots ──
    def _on_frame(self, image) -> None:
        if self.worker is None:  # ignore stray frames after stopping
            return
        if not self._got_frame:
            self._got_frame = True
            self.status_changed.emit("live")

        if self.detections:
            draw_detections(image, self.detections)
        if self.text_blocks:
            draw_text_blocks(image, self.text_blocks)

        pixmap = QPixmap.fromImage(image)
        self.video_label.setPixmap(
            pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def _on_frame_np(self, frame) -> None:
        self.last_frame = frame
        if self.vision is not None:
            self.vision.submit(frame)
        if self.ocr is not None:
            self.ocr.submit(frame)
        if self.scene is not None:
            self.scene.submit(frame, [d["label"] for d in self.detections])

    def _on_results(self, detections) -> None:
        self.detections = detections
        self.detections_changed.emit(detections)

    def _on_ocr(self, blocks) -> None:
        self.text_blocks = blocks
        self.text_changed.emit(blocks)

    def _on_error(self, message) -> None:
        self._stop_worker()
        self.error_label.setText(message)
        self.stack.setCurrentIndex(2)
        self.status_changed.emit("error")

    # ── helpers ──
    @staticmethod
    def _center(label: QLabel, object_name: str) -> QLabel:
        label.setObjectName(object_name)
        label.setAlignment(Qt.AlignCenter)
        return label

    @staticmethod
    def _button_row(button: QPushButton) -> QHBoxLayout:
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(button)
        row.addStretch(1)
        return row
