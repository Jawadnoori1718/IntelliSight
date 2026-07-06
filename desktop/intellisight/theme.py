"""Dark, neon-accented theme for the desktop app (Qt Style Sheets)."""

# Palette (kept in sync with the web version's look)
BG = "#05070e"
TEXT = "#e8eefb"
TEXT_DIM = "#97a7c4"
TEXT_FAINT = "#5a6a86"
ACCENT = "#38bdf8"
ACCENT_2 = "#6366f1"
OK = "#34d399"
WARN = "#fbbf24"
DANGER = "#f87171"

STYLE = f"""
QMainWindow {{ background-color: {BG}; }}
QWidget {{
    color: {TEXT};
    font-family: "Helvetica Neue", "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}}

/* Header */
QFrame#Header {{
    background-color: rgba(20, 27, 44, 0.65);
    border: 1px solid rgba(120, 160, 255, 0.14);
    border-radius: 16px;
}}
QLabel#BrandBadge {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {ACCENT}, stop:1 {ACCENT_2});
    border-radius: 11px;
    font-size: 20px;
}}
QLabel#BrandTitle {{ font-size: 20px; font-weight: 700; color: #ffffff; }}
QLabel#BrandSub {{ color: {TEXT_FAINT}; font-size: 10px; letter-spacing: 2px; }}
QLabel#StatusPill {{
    background-color: rgba(251, 191, 36, 0.10);
    color: {WARN};
    border: 1px solid rgba(251, 191, 36, 0.35);
    border-radius: 13px;
    padding: 6px 14px;
    font-weight: 600;
    font-size: 12px;
}}

/* Camera stage */
QFrame#Stage {{
    background-color: rgba(20, 27, 44, 0.45);
    border: 1px solid rgba(120, 160, 255, 0.14);
    border-radius: 20px;
}}
QLabel#StageTitle {{ color: {TEXT}; font-size: 17px; font-weight: 600; }}
QLabel#StageHint {{ color: {TEXT_DIM}; font-size: 13px; }}
QLabel#StageIcon {{ font-size: 46px; }}

/* Sidebar panels */
QFrame[panel="true"] {{
    background-color: rgba(20, 27, 44, 0.5);
    border: 1px solid rgba(120, 160, 255, 0.14);
    border-radius: 16px;
}}
QLabel#PanelTitle {{ font-size: 14px; font-weight: 600; color: {TEXT}; }}
QLabel#PanelBody {{ color: {TEXT_DIM}; font-size: 13px; }}

/* Scrollbars */
QScrollBar:vertical {{ background: transparent; width: 8px; margin: 0; }}
QScrollBar::handle:vertical {{ background: rgba(120, 160, 255, 0.18); border-radius: 4px; min-height: 24px; }}
QScrollBar::handle:vertical:hover {{ background: rgba(120, 160, 255, 0.34); }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""


def apply_theme(app):
    """Apply the IntelliSight dark theme to a QApplication."""
    app.setStyleSheet(STYLE)
