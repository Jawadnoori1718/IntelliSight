"""Big Brother Desktop — application entry point.

Run it with:
    python -m bigbrother.app
or:
    ./run.sh
"""

import sys

from PySide6.QtWidgets import QApplication

from .brandmark import make_icon
from .main_window import MainWindow
from .theme import apply_theme


def create_app():
    """Create the QApplication and main window (no event loop started yet)."""
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Big Brother")
    app.setWindowIcon(make_icon())
    apply_theme(app)
    window = MainWindow()
    return app, window


def main():
    app, window = create_app()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
