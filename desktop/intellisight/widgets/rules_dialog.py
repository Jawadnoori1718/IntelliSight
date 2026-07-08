"""A dialog to build, list, toggle, and delete rules."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

TRIGGERS = [
    ("Appears", "appears"),
    ("Disappears", "disappears"),
    ("Lingers (8s+)", "lingers"),
    ("Enters the zone", "enters_zone"),
    ("Count in zone ≥", "count_over"),
]
ACTIONS = [
    ("Show an alert", "alert"),
    ("Play a sound", "sound"),
    ("Save a snapshot", "snapshot"),
]


class RulesDialog(QDialog):
    changed = Signal()

    def __init__(self, engine, labels, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setObjectName("RulesDialog")
        self.setWindowTitle("Rules")
        self.setModal(True)
        self.setMinimumWidth(500)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 22, 24, 22)
        root.setSpacing(14)

        header = QLabel("Rules")
        header.setObjectName("RulesHeader")
        subtitle = QLabel("When the camera sees something, do something.")
        subtitle.setObjectName("RulesSub")
        root.addWidget(header)
        root.addWidget(subtitle)

        # Existing rules
        self._list = QVBoxLayout()
        self._list.setContentsMargins(0, 0, 0, 0)
        self._list.setSpacing(8)
        container = QWidget()
        container.setLayout(self._list)
        container.setStyleSheet("background: transparent;")
        scroll = QScrollArea()
        scroll.setObjectName("RulesScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(container)
        scroll.setMinimumHeight(160)
        scroll.viewport().setStyleSheet("background: transparent;")
        root.addWidget(scroll, 1)

        # Builder
        builder = QVBoxLayout()
        builder.setSpacing(10)

        row1 = QHBoxLayout()
        row1.setSpacing(8)
        when = QLabel("When")
        when.setObjectName("RuleWord")
        self.obj_combo = QComboBox()
        self.obj_combo.setEditable(True)
        self.obj_combo.addItem("Anything")
        self.obj_combo.addItems(labels)
        self.trigger_combo = QComboBox()
        for text, value in TRIGGERS:
            self.trigger_combo.addItem(text, value)
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(1, 20)
        self.threshold_spin.setValue(2)
        self.threshold_spin.hide()
        row1.addWidget(when)
        row1.addWidget(self.obj_combo, 1)
        row1.addWidget(self.trigger_combo, 1)
        row1.addWidget(self.threshold_spin)
        builder.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(8)
        then = QLabel("Then")
        then.setObjectName("RuleWord")
        self.action_combo = QComboBox()
        for text, value in ACTIONS:
            self.action_combo.addItem(text, value)
        add_btn = QPushButton("＋  Add Rule")
        add_btn.setObjectName("AddRuleBtn")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self._add)
        row2.addWidget(then)
        row2.addWidget(self.action_combo, 1)
        row2.addStretch(1)
        row2.addWidget(add_btn)
        builder.addLayout(row2)

        root.addLayout(builder)

        self.trigger_combo.currentIndexChanged.connect(self._on_trigger_changed)
        self._refresh()

    # ── builder ──
    def _on_trigger_changed(self) -> None:
        is_count = self.trigger_combo.currentData() == "count_over"
        self.threshold_spin.setVisible(is_count)
        self.obj_combo.setEnabled(not is_count)

    def _add(self) -> None:
        trigger = self.trigger_combo.currentData()
        action = self.action_combo.currentData()
        text = self.obj_combo.currentText().strip()
        obj = None if (not text or text.lower() == "anything") else text.lower()
        if trigger == "count_over":
            obj = None
        self.engine.add(obj, trigger, action, self.threshold_spin.value())
        self._refresh()
        self.changed.emit()

    # ── list ──
    def _clear_list(self) -> None:
        while self._list.count():
            item = self._list.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _refresh(self) -> None:
        self._clear_list()
        if not self.engine.rules:
            empty = QLabel("No rules yet — build one below.")
            empty.setObjectName("RulesEmpty")
            self._list.addWidget(empty)
            self._list.addStretch(1)
            return
        for rule in self.engine.rules:
            self._list.addWidget(self._rule_row(rule))
        self._list.addStretch(1)

    def _rule_row(self, rule) -> QFrame:
        item = QFrame()
        item.setObjectName("RuleItem")
        row = QHBoxLayout(item)
        row.setContentsMargins(12, 8, 12, 8)
        row.setSpacing(10)

        check = QCheckBox()
        check.setChecked(rule.enabled)
        check.setCursor(Qt.PointingHandCursor)
        check.toggled.connect(lambda on, r=rule: self._toggle(r, on))

        desc = QLabel(rule.describe())
        desc.setObjectName("RuleDesc")
        desc.setWordWrap(True)

        remove = QPushButton("Remove")
        remove.setObjectName("RemoveRuleBtn")
        remove.setCursor(Qt.PointingHandCursor)
        remove.clicked.connect(lambda _=False, rid=rule.id: self._delete(rid))

        row.addWidget(check)
        row.addWidget(desc, 1)
        row.addWidget(remove)
        return item

    def _toggle(self, rule, enabled) -> None:
        rule.enabled = bool(enabled)
        self.changed.emit()

    def _delete(self, rule_id) -> None:
        self.engine.remove(rule_id)
        self._refresh()
        self.changed.emit()
