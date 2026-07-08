"""The camera stage: a full-bleed video with sleek glass overlays on top.

Idle → a centered start screen. Live → the video fills the frame while a brand
mark, a status pill, a 'Detected' card, and a Stop button float over it. Error →
a centered message. The overlays are children of the stage (not in a layout) so
they can sit on top of the video; they're repositioned on every resize.
"""

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

from ..brandmark import BrandMark
from ..camera import CameraWorker
from ..overlay import draw_detections
from ..vision_worker import VisionWorker
from .objects_overlay import ObjectsOverlay

MARGIN = 20  # gap between the floating overlays and the video edges


class CameraStage(QFrame):
    """Owns the camera + vision workers and swaps between idle / live / error."""

    status_changed = Signal(str)         # idle | starting | live | error
    detections_changed = Signal(object)  # list[detection]
    vision_status_changed = Signal(str)  # loading | ready | error

    def __init__(self):
        super().__init__()
        self.setObjectName("Stage")
        self.worker = None
        self.vision = None
        self.detections = []
        self._got_frame = False

        self.stack = QStackedWidget()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self.stack)

        self.stack.addWidget(self._build_idle())   # 0
        self.stack.addWidget(self._build_live())   # 1
        self.stack.addWidget(self._build_error())  # 2
        self.stack.setCurrentIndex(0)

        self._build_overlays()
        self._show_overlays(False)

    # ── pages ──
    def _build_idle(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.addStretch(1)
        lay.addWidget(self._center_widget(BrandMark(60)))
        lay.addSpacing(18)
        lay.addWidget(self._center(QLabel("Big Brother"), "StartTitle"))
        lay.addWidget(self._center(QLabel("Always watching — point it at anything."), "StartHint"))
        lay.addSpacing(24)
        start = QPushButton("Start Camera")
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
        self.video_label = QLabel()
        self.video_label.setObjectName("VideoLabel")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setMinimumSize(1, 1)
        lay.addWidget(self.video_label)
        return page

    def _build_error(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.addStretch(1)
        lay.addWidget(self._center(QLabel("⚠️"), "ErrorIcon"))
        lay.addSpacing(10)
        lay.addWidget(self._center(QLabel("Couldn't start the camera"), "ErrorTitle"))
        self.error_label = QLabel("")
        self.error_label.setObjectName("ErrorText")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        lay.addWidget(self.error_label)
        lay.addSpacing(20)
        retry = QPushButton("Try Again")
        retry.setObjectName("StartBtn")
        retry.setCursor(Qt.PointingHandCursor)
        retry.clicked.connect(self.start_camera)
        lay.addLayout(self._button_row(retry))
        lay.addStretch(1)
        return page

    # ── floating overlays ──
    def _build_overlays(self) -> None:
        # Brand (top-left)
        self.brand = QFrame(self)
        self.brand.setObjectName("BrandOverlay")
        brow = QHBoxLayout(self.brand)
        brow.setContentsMargins(12, 8, 16, 8)
        brow.setSpacing(10)
        brow.addWidget(BrandMark(26))
        brow.addWidget(self._plain(QLabel("Big Brother"), "BrandName"))

        # Status pill (top-right)
        self.pill = QLabel("● CONNECTING", self)
        self.pill.setObjectName("LiveOverlay")
        self.pill.setProperty("state", "connecting")

        # Detected-objects card (top-right, under the pill)
        self.objects = ObjectsOverlay(self)

        # Stop button (bottom-center)
        self.stop_btn = QPushButton("■  Stop", self)
        self.stop_btn.setObjectName("StopFloat")
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.clicked.connect(self.stop_camera)

        self._overlays = [self.brand, self.pill, self.objects, self.stop_btn]

    def _show_overlays(self, visible: bool) -> None:
        for widget in self._overlays:
            widget.setVisible(visible)
        if visible:
            for widget in self._overlays:
                widget.raise_()
            self._position_overlays()

    def _position_overlays(self) -> None:
        w, h = self.width(), self.height()

        self.brand.adjustSize()
        self.brand.move(MARGIN, MARGIN)

        self.pill.adjustSize()
        self.pill.move(w - self.pill.width() - MARGIN, MARGIN)

        self.objects.adjustSize()
        self.objects.move(
            w - self.objects.width() - MARGIN,
            MARGIN + self.pill.height() + 12,
        )

        self.stop_btn.adjustSize()
        self.stop_btn.move((w - self.stop_btn.width()) // 2, h - self.stop_btn.height() - MARGIN)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self.brand.isVisible():
            self._position_overlays()

    # ── status pill ──
    def _set_pill(self, state: str, text: str) -> None:
        self.pill.setText(text)
        self.pill.setProperty("state", state)
        self.pill.style().unpolish(self.pill)
        self.pill.style().polish(self.pill)
        self._position_overlays()

    # ── controls ──
    def start_camera(self) -> None:
        if self.worker is not None:
            return
        self._got_frame = False
        self.detections = []
        self.objects.set_message("Warming up…")
        self._set_pill("connecting", "● CONNECTING")
        self.status_changed.emit("starting")
        self.stack.setCurrentIndex(1)
        self._show_overlays(True)

        self.worker = CameraWorker(0)
        self.worker.frame_ready.connect(self._on_frame)
        self.worker.frame_np.connect(self._on_frame_np)
        self.worker.error.connect(self._on_error)

        self.vision = VisionWorker()
        self.vision.results_ready.connect(self._on_results)
        self.vision.status.connect(self._on_vision_status)

        self.worker.start()
        self.vision.start()

    def stop_camera(self) -> None:
        self._stop_workers()
        self._show_overlays(False)
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

    # ── slots ──
    def _on_frame(self, image) -> None:
        if self.worker is None:
            return
        if not self._got_frame:
            self._got_frame = True
            self._set_pill("live", "● LIVE")
            self.status_changed.emit("live")
        if self.detections:
            draw_detections(image, self.detections)
        pixmap = QPixmap.fromImage(image)
        self.video_label.setPixmap(
            pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def _on_frame_np(self, frame) -> None:
        if self.vision is not None:
            self.vision.submit(frame)

    def _on_results(self, detections) -> None:
        self.detections = detections
        self.objects.update(detections)
        self._position_overlays()
        self.detections_changed.emit(detections)

    def _on_vision_status(self, state) -> None:
        if state == "loading":
            self.objects.set_message("Loading detector…")
        elif state == "error":
            self.objects.set_message("Detector failed to load.")
        self._position_overlays()
        self.vision_status_changed.emit(state)

    def _on_error(self, message) -> None:
        self._stop_workers()
        self._show_overlays(False)
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
    def _plain(label: QLabel, object_name: str) -> QLabel:
        label.setObjectName(object_name)
        return label

    @staticmethod
    def _center_widget(widget: QWidget) -> QWidget:
        holder = QWidget()
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 0, 0, 0)
        row.addStretch(1)
        row.addWidget(widget)
        row.addStretch(1)
        return holder

    @staticmethod
    def _button_row(button: QPushButton) -> QHBoxLayout:
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(button)
        row.addStretch(1)
        return row
