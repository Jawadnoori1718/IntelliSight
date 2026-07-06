"""The 'Live Stats' sidebar panel — a small grid of live metric tiles."""

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout


class StatTile(QFrame):
    def __init__(self, name: str):
        super().__init__()
        self.setObjectName("StatTile")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(11, 8, 11, 8)
        layout.setSpacing(2)

        self.value = QLabel("—")
        self.value.setObjectName("StatValue")
        caption = QLabel(name.upper())
        caption.setObjectName("StatName")

        layout.addWidget(self.value)
        layout.addWidget(caption)

    def set_value(self, text: str) -> None:
        self.value.setText(text)


class StatsPanel(QFrame):
    _SPECS = [
        ("fps", "FPS"),
        ("objects", "Objects"),
        ("people", "People"),
        ("inference", "Inference"),
        ("cpu", "CPU"),
        ("confidence", "Confidence"),
    ]

    def __init__(self):
        super().__init__()
        self.setProperty("panel", True)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 14, 16, 16)
        outer.setSpacing(12)

        title = QLabel("Live Stats")
        title.setObjectName("PanelTitle")
        outer.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(8)
        self.tiles = {}
        for index, (key, label) in enumerate(self._SPECS):
            tile = StatTile(label)
            self.tiles[key] = tile
            grid.addWidget(tile, index // 2, index % 2)
        outer.addLayout(grid)

    def set(self, key: str, text: str) -> None:
        if key in self.tiles:
            self.tiles[key].set_value(text)

    def reset(self) -> None:
        for tile in self.tiles.values():
            tile.set_value("—")
