"""The camera stage: a full-bleed video with sleek glass overlays on top.

Idle → a centered start screen. Live → the video fills the frame while a brand
mark, a status pill, a 'Detected' card, and a Stop button float over it. Error →
a centered message. The overlays are children of the stage (not in a layout) so
they can sit on top of the video; they're repositioned on every resize.
"""

import subprocess
import time
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
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
from ..events import EventDetector
from ..notifications import Notifier
from ..overlay import draw_detections, draw_zone
from ..rules import RulesEngine
from ..storage import Timeline
from ..vision_worker import VisionWorker
from ..webhooks import send_webhook
from .event_feed import EventFeed
from .objects_overlay import ObjectsOverlay
from .rules_dialog import RulesDialog
from .timeline_dialog import TimelineDialog

MARGIN = 20  # gap between the floating overlays and the video edges
MIN_ZONE = 0.03  # a drag smaller than this (a click) clears the zone instead


def _norm_rect(a, b):
    x1, x2 = sorted((a[0], b[0]))
    y1, y2 = sorted((a[1], b[1]))
    return (x1, y1, x2, y2)


class VideoLabel(QLabel):
    """The video surface — the user drags a rectangular counting zone on it."""

    zone_updated = Signal(object)  # (x1, y1, x2, y2) normalised, or None to clear

    def __init__(self):
        super().__init__()
        self._area = None        # displayed-image rect in widget coordinates
        self._drag_start = None  # normalised start point
        self._dragging = False
        self.setCursor(Qt.CrossCursor)

    def set_image_area(self, rect: QRectF) -> None:
        self._area = rect

    def _to_norm(self, pos):
        area = self._area
        if area is None or area.width() <= 0 or area.height() <= 0:
            return None
        nx = (pos.x() - area.x()) / area.width()
        ny = (pos.y() - area.y()) / area.height()
        return (min(1.0, max(0.0, nx)), min(1.0, max(0.0, ny)))

    def mousePressEvent(self, event) -> None:
        point = self._to_norm(event.position())
        if point is None:
            return
        self._drag_start = point
        self._dragging = True

    def mouseMoveEvent(self, event) -> None:
        if not self._dragging or self._drag_start is None:
            return
        point = self._to_norm(event.position())
        if point is not None:
            self.zone_updated.emit(_norm_rect(self._drag_start, point))

    def mouseReleaseEvent(self, event) -> None:
        if not self._dragging:
            return
        self._dragging = False
        point = self._to_norm(event.position())
        start, self._drag_start = self._drag_start, None
        if point is None or start is None:
            return
        x1, y1, x2, y2 = _norm_rect(start, point)
        if (x2 - x1) < MIN_ZONE or (y2 - y1) < MIN_ZONE:
            self.zone_updated.emit(None)  # a click (not a drag) clears the zone
        else:
            self.zone_updated.emit((x1, y1, x2, y2))


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
        self.zone = None        # (x1, y1, x2, y2) normalised, or None
        self.zone_count = 0
        self.event_detector = EventDetector()
        self.rules_engine = RulesEngine()
        self.notifier = Notifier()
        self.timeline = Timeline()
        self._last_image = None
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
        self.video_label = VideoLabel()
        self.video_label.setObjectName("VideoLabel")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setMinimumSize(1, 1)
        self.video_label.zone_updated.connect(self._on_zone_updated)
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

        # Activity feed (top-left, under the brand)
        self.event_feed = EventFeed(self)

        # Detected-objects card (top-right, under the pill)
        self.objects = ObjectsOverlay(self)

        # Rules button (bottom-left)
        self.rules_btn = QPushButton("⚙  Rules", self)
        self.rules_btn.setObjectName("RulesButton")
        self.rules_btn.setCursor(Qt.PointingHandCursor)
        self.rules_btn.clicked.connect(self._open_rules)

        # Timeline button (bottom-right)
        self.timeline_btn = QPushButton("🕓  Timeline", self)
        self.timeline_btn.setObjectName("TimelineButton")
        self.timeline_btn.setCursor(Qt.PointingHandCursor)
        self.timeline_btn.clicked.connect(self._open_timeline)

        # Stop button (bottom-center)
        self.stop_btn = QPushButton("■  Stop", self)
        self.stop_btn.setObjectName("StopFloat")
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.clicked.connect(self.stop_camera)

        # Toast banner (top-center, shown briefly when a rule fires)
        self.toast = QLabel("", self)
        self.toast.setObjectName("Toast")
        self.toast.setAlignment(Qt.AlignCenter)
        self.toast.hide()
        self._toast_timer = QTimer(self)
        self._toast_timer.setSingleShot(True)
        self._toast_timer.timeout.connect(self.toast.hide)

        # Zone hint / clear (bottom-center, just above Stop)
        self.zone_hint = QLabel("⬚  Drag on the video to draw a counting zone", self)
        self.zone_hint.setObjectName("ZoneHint")
        self.clear_zone_btn = QPushButton("✕  Clear Zone", self)
        self.clear_zone_btn.setObjectName("ZoneClear")
        self.clear_zone_btn.setCursor(Qt.PointingHandCursor)
        self.clear_zone_btn.clicked.connect(lambda: self._on_zone_updated(None))

        self._overlays = [
            self.brand, self.event_feed, self.pill, self.objects,
            self.rules_btn, self.timeline_btn, self.stop_btn,
        ]
        self._zone_controls = [self.zone_hint, self.clear_zone_btn]
        self._update_rules_button()

    def _show_overlays(self, visible: bool) -> None:
        for widget in self._overlays:
            widget.setVisible(visible)
        if visible:
            self._update_zone_controls()
            for widget in self._overlays + self._zone_controls:
                widget.raise_()
            self._position_overlays()
        else:
            for widget in self._zone_controls:
                widget.setVisible(False)
            self.toast.hide()

    def _position_overlays(self) -> None:
        w, h = self.width(), self.height()

        self.brand.adjustSize()
        self.brand.move(MARGIN, MARGIN)

        self.event_feed.adjustSize()
        self.event_feed.move(MARGIN, MARGIN + self.brand.height() + 12)

        self.pill.adjustSize()
        self.pill.move(w - self.pill.width() - MARGIN, MARGIN)

        self.objects.adjustSize()
        self.objects.move(
            w - self.objects.width() - MARGIN,
            MARGIN + self.pill.height() + 12,
        )

        self.stop_btn.adjustSize()
        self.stop_btn.move((w - self.stop_btn.width()) // 2, h - self.stop_btn.height() - MARGIN)

        self.rules_btn.adjustSize()
        self.rules_btn.move(MARGIN, h - self.rules_btn.height() - MARGIN)

        self.timeline_btn.adjustSize()
        self.timeline_btn.move(
            w - self.timeline_btn.width() - MARGIN, h - self.timeline_btn.height() - MARGIN
        )

        above_stop = h - self.stop_btn.height() - MARGIN - 10
        self.zone_hint.adjustSize()
        self.zone_hint.move((w - self.zone_hint.width()) // 2, above_stop - self.zone_hint.height())
        self.clear_zone_btn.adjustSize()
        self.clear_zone_btn.move(
            (w - self.clear_zone_btn.width()) // 2, above_stop - self.clear_zone_btn.height()
        )

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self.brand.isVisible():
            self._position_overlays()

    # ── counting zone ──
    def _on_zone_updated(self, zone) -> None:
        self.zone = zone
        self._recompute_zone_count()
        self._update_zone_controls()
        self._position_overlays()

    def _recompute_zone_count(self) -> None:
        if not self.zone:
            self.zone_count = 0
            return
        x1, y1, x2, y2 = self.zone
        count = 0
        for det in self.detections:
            box = det["box"]
            cx = (box["x1"] + box["x2"]) / 2
            cy = (box["y1"] + box["y2"]) / 2
            if x1 <= cx <= x2 and y1 <= cy <= y2:
                count += 1
        self.zone_count = count

    def _update_zone_controls(self) -> None:
        live = self.stack.currentIndex() == 1
        self.zone_hint.setVisible(live and self.zone is None)
        self.clear_zone_btn.setVisible(live and self.zone is not None)

    # ── rules ──
    def _open_rules(self) -> None:
        dialog = RulesDialog(self.rules_engine, self._known_labels(), self.notifier, self)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.changed.connect(self._update_rules_button)
        dialog.exec()
        self._update_rules_button()

    def _open_timeline(self) -> None:
        dialog = TimelineDialog(self.timeline, self)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.exec()

    def _known_labels(self) -> list:
        common = ["person", "phone", "laptop", "dog", "cat", "cup", "bottle", "backpack", "keys", "book"]
        seen = [det["label"].lower() for det in self.detections]
        return [name.title() for name in sorted(set(common + seen))]

    def _update_rules_button(self) -> None:
        count = len(self.rules_engine.rules)
        self.rules_btn.setText(f"⚙  Rules  ·  {count}" if count else "⚙  Rules")
        self.rules_btn.adjustSize()
        if self.brand.isVisible():
            self._position_overlays()

    def _fire_rule(self, firing) -> None:
        rule = firing["rule"]
        text = firing["text"]
        self.event_feed.add({"type": "rule", "label": f"⚡ {text}"})
        snapshot = None
        if rule.action == "alert":
            self._show_toast(f"⚡  {text}")
        elif rule.action == "notify":
            self.notifier.send("Big Brother", text)
            self._show_toast(f"🔔  {text}")
        elif rule.action == "sound":
            self._play_sound()
        elif rule.action == "snapshot":
            snapshot = self._save_snapshot()
        elif rule.action == "webhook":
            send_webhook(rule.url, {
                "app": "Big Brother",
                "text": text,
                "trigger": rule.trigger,
                "object": rule.obj or "anything",
                "rule": rule.describe(),
                "time": datetime.now().isoformat(timespec="seconds"),
            })
            self._show_toast(f"🔌  {text}")
        self.timeline.add("rule", text, None, snapshot)

    def _show_toast(self, text: str) -> None:
        self.toast.setText(text)
        self.toast.adjustSize()
        self.toast.move((self.width() - self.toast.width()) // 2, MARGIN)
        self.toast.show()
        self.toast.raise_()
        self._toast_timer.start(2600)

    def _play_sound(self) -> None:
        try:
            subprocess.Popen(["afplay", "/System/Library/Sounds/Glass.aiff"])
        except Exception:
            QApplication.beep()

    def _save_snapshot(self):
        if self._last_image is None:
            return None
        folder = Path.home() / "BigBrother Snapshots"
        folder.mkdir(parents=True, exist_ok=True)
        name = f"snapshot-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.png"
        path = str(folder / name)
        if self._last_image.save(path):
            self._show_toast("📸  Snapshot saved")
            return path
        return None

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
        self.zone = None
        self.zone_count = 0
        self._last_image = None
        self.event_detector.reset()
        self.rules_engine.reset_state()
        self.event_feed.clear()
        self.toast.hide()
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
        self.timeline.close()

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
        if self.zone:
            draw_zone(image, self.zone, self.zone_count)
        self._last_image = image

        pixmap = QPixmap.fromImage(image)
        scaled = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        offset_x = (self.video_label.width() - scaled.width()) / 2
        offset_y = (self.video_label.height() - scaled.height()) / 2
        self.video_label.set_image_area(QRectF(offset_x, offset_y, scaled.width(), scaled.height()))
        self.video_label.setPixmap(scaled)

    def _on_frame_np(self, frame) -> None:
        if self.vision is not None:
            self.vision.submit(frame)

    def _on_results(self, detections) -> None:
        if self.vision is None:
            return
        self.detections = detections
        self.objects.update(detections)
        self._recompute_zone_count()

        now = time.monotonic()
        events = self.event_detector.update(detections, now)
        for event in events:
            self.event_feed.add(event)
            self.timeline.add(event["type"], event["label"], event.get("category"))
        for firing in self.rules_engine.evaluate(events, detections, self.zone, self.zone_count, now):
            self._fire_rule(firing)

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
