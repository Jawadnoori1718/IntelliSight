"""The 'Current Scene' panel — an AI description plus activity/environment chips."""

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class ScenePanel(QFrame):
    _CHIP_KEYS = ("activity", "environment", "lighting")

    def __init__(self):
        super().__init__()
        self.setProperty("panel", True)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 14, 16, 16)
        outer.setSpacing(10)

        head = QHBoxLayout()
        title = QLabel("Current Scene")
        title.setObjectName("PanelTitle")
        self.status = QLabel("")
        self.status.setObjectName("SceneStatus")
        head.addWidget(title)
        head.addStretch(1)
        head.addWidget(self.status)
        outer.addLayout(head)

        self.description = QLabel("Waiting for the camera…")
        self.description.setObjectName("PanelBody")
        self.description.setWordWrap(True)
        outer.addWidget(self.description)

        chips = QHBoxLayout()
        chips.setSpacing(6)
        self.chips = {}
        for key in self._CHIP_KEYS:
            chip = QLabel("")
            chip.setObjectName("SceneChip")
            chip.hide()
            self.chips[key] = chip
            chips.addWidget(chip)
        chips.addStretch(1)
        outer.addLayout(chips)

    def set_status(self, text: str) -> None:
        self.status.setText(text)

    def set_scene(self, data: dict) -> None:
        self.description.setText(data.get("description") or "…")
        for key, chip in self.chips.items():
            value = (data.get(key) or "").strip()
            if value and value != "—":
                chip.setText(value)
                chip.show()
            else:
                chip.hide()

    def set_message(self, text: str) -> None:
        self.description.setText(text)
        self.status.setText("")
        for chip in self.chips.values():
            chip.hide()
