"""A dialog to build, list, toggle, and delete rules."""

from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..webhooks import send_webhook

TRIGGERS = [
    ("Appears", "appears"),
    ("Disappears", "disappears"),
    ("Lingers (8s+)", "lingers"),
    ("Enters the zone", "enters_zone"),
    ("Count in zone ≥", "count_over"),
]
ACTIONS = [
    ("Show an alert", "alert"),
    ("Notify me (desktop + phone)", "notify"),
    ("Play a sound", "sound"),
    ("Save a snapshot", "snapshot"),
    ("Send a webhook", "webhook"),
]


class RulesDialog(QDialog):
    changed = Signal()

    def __init__(self, engine, labels, notifier, claude, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.notifier = notifier
        self.claude = claude
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

        url_row = QHBoxLayout()
        url_row.setSpacing(8)
        self._url_word = QLabel("URL")
        self._url_word.setObjectName("RuleWord")
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://…  (Home Assistant, Slack, your script)")
        url_test = QPushButton("Test")
        url_test.setObjectName("SmallBtn")
        url_test.setCursor(Qt.PointingHandCursor)
        url_test.clicked.connect(self._test_webhook)
        url_row.addWidget(self._url_word)
        url_row.addWidget(self.url_edit, 1)
        url_row.addWidget(url_test)
        builder.addLayout(url_row)
        self._url_widgets = [self._url_word, self.url_edit, url_test]
        for widget in self._url_widgets:
            widget.hide()

        check_row = QHBoxLayout()
        check_row.setSpacing(8)
        check_word = QLabel("Only if")
        check_word.setObjectName("RuleWord")
        self.check_edit = QLineEdit()
        self.check_edit.setPlaceholderText(
            "(optional) Claude confirms this on the live frame — e.g. the person is holding a package"
        )
        check_row.addWidget(check_word)
        check_row.addWidget(self.check_edit, 1)
        builder.addLayout(check_row)

        root.addLayout(builder)

        # Notifications settings
        settings_title = QLabel("NOTIFICATIONS")
        settings_title.setObjectName("SettingsTitle")
        root.addSpacing(4)
        root.addWidget(settings_title)

        self.desktop_check = QCheckBox("Show macOS notifications")
        self.desktop_check.setChecked(self.notifier.desktop_enabled)
        self.desktop_check.setCursor(Qt.PointingHandCursor)
        self.desktop_check.toggled.connect(self.notifier.set_desktop)
        root.addWidget(self.desktop_check)

        phone_row = QHBoxLayout()
        phone_row.setSpacing(8)
        self.topic_edit = QLineEdit(self.notifier.ntfy_topic)
        self.topic_edit.setPlaceholderText("Phone push topic (ntfy.sh) — e.g. bigbrother-7h2k")
        self.topic_edit.textChanged.connect(self.notifier.set_topic)
        test_btn = QPushButton("Test")
        test_btn.setObjectName("SmallBtn")
        test_btn.setCursor(Qt.PointingHandCursor)
        test_btn.clicked.connect(self._test)
        phone_row.addWidget(self.topic_edit, 1)
        phone_row.addWidget(test_btn)
        root.addLayout(phone_row)

        help_label = QLabel(
            "For phone alerts: install the free ntfy app, subscribe to this topic, and Big "
            "Brother will ping your phone. Leave blank to keep it desktop-only."
        )
        help_label.setObjectName("SettingsHelp")
        help_label.setWordWrap(True)
        root.addWidget(help_label)

        # Claude verification settings
        claude_title = QLabel("CLAUDE VERIFICATION")
        claude_title.setObjectName("SettingsTitle")
        root.addSpacing(4)
        root.addWidget(claude_title)

        self.claude_status = QLabel()
        self.claude_status.setObjectName("SettingsHelp")
        root.addWidget(self.claude_status)

        key_row = QHBoxLayout()
        key_row.setSpacing(8)
        key_word = QLabel("Key")
        key_word.setObjectName("RuleWord")
        self.key_edit = QLineEdit(self.claude.stored_key())
        self.key_edit.setEchoMode(QLineEdit.Password)
        self.key_edit.setPlaceholderText("Anthropic API key (sk-ant-…)")
        self.key_edit.textChanged.connect(self._on_key_changed)
        if self.claude.key_from_env():
            self.key_edit.setDisabled(True)
            self.key_edit.setPlaceholderText("Using ANTHROPIC_API_KEY from environment")
        cap_word = QLabel("Max / hr")
        cap_word.setObjectName("RuleWord")
        self.cap_spin = QSpinBox()
        self.cap_spin.setRange(1, 600)
        self.cap_spin.setValue(self.claude.max_per_hour)
        self.cap_spin.valueChanged.connect(self.claude.set_max)
        key_row.addWidget(key_word)
        key_row.addWidget(self.key_edit, 1)
        key_row.addWidget(cap_word)
        key_row.addWidget(self.cap_spin)
        root.addLayout(key_row)

        claude_help = QLabel(
            "Give a rule an 'Only if' condition above and Claude confirms it on the live frame "
            "before acting. Uses your Anthropic key — a few cents per check, capped per hour."
        )
        claude_help.setObjectName("SettingsHelp")
        claude_help.setWordWrap(True)
        root.addWidget(claude_help)
        self._update_claude_status()

        self.trigger_combo.currentIndexChanged.connect(self._on_trigger_changed)
        self.action_combo.currentIndexChanged.connect(self._on_action_changed)
        self._refresh()

    def _on_key_changed(self, text) -> None:
        self.claude.set_key(text)
        self._update_claude_status()

    def _update_claude_status(self) -> None:
        state = self.claude.status()
        if state == "ready":
            suffix = " (environment key)" if self.claude.key_from_env() else ""
            self.claude_status.setText(f"✓ Ready to verify{suffix}")
        elif state == "nokey":
            self.claude_status.setText("Add your Anthropic API key below to enable Claude checks.")
        else:
            self.claude_status.setText("The 'anthropic' package isn't installed — run: pip install anthropic")

    def _test(self) -> None:
        self.notifier.send("Big Brother", "Test notification 🔔")

    def _on_action_changed(self) -> None:
        is_webhook = self.action_combo.currentData() == "webhook"
        for widget in self._url_widgets:
            widget.setVisible(is_webhook)

    def _test_webhook(self) -> None:
        send_webhook(
            self.url_edit.text(),
            {"app": "Big Brother", "text": "Test webhook",
             "time": datetime.now().isoformat(timespec="seconds")},
        )

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
        url = self.url_edit.text().strip() if action == "webhook" else ""
        check = self.check_edit.text().strip()
        self.engine.add(obj, trigger, action, self.threshold_spin.value(), url, check)
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
