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
QLabel#StatusPill[state="live"] {{
    background-color: rgba(52, 211, 153, 0.12);
    color: {OK};
    border: 1px solid rgba(52, 211, 153, 0.40);
}}
QLabel#StatusPill[state="error"] {{
    background-color: rgba(248, 113, 113, 0.12);
    color: {DANGER};
    border: 1px solid rgba(248, 113, 113, 0.40);
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
QLabel#VideoLabel {{ background-color: #04060c; border-radius: 14px; }}
QLabel#ErrorText {{ color: {DANGER}; font-size: 13px; }}

/* Buttons */
QPushButton#StartBtn {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {ACCENT}, stop:1 {ACCENT_2});
    color: #04121e;
    border: none;
    border-radius: 12px;
    padding: 11px 22px;
    font-size: 14px;
    font-weight: 600;
}}
QPushButton#StartBtn:hover {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4cc5fb, stop:1 #7278f2);
}}
QPushButton#StopBtn {{
    background-color: rgba(248, 113, 113, 0.12);
    color: {DANGER};
    border: 1px solid rgba(248, 113, 113, 0.35);
    border-radius: 10px;
    padding: 8px 18px;
    font-size: 12px;
    font-weight: 600;
}}
QPushButton#StopBtn:hover {{ background-color: rgba(248, 113, 113, 0.20); }}

/* Sidebar panels */
QFrame[panel="true"] {{
    background-color: rgba(20, 27, 44, 0.5);
    border: 1px solid rgba(120, 160, 255, 0.14);
    border-radius: 16px;
}}
QLabel#PanelTitle {{ font-size: 14px; font-weight: 600; color: {TEXT}; }}
QLabel#PanelBody {{ color: {TEXT_DIM}; font-size: 13px; }}

/* Stat tiles */
QFrame#StatTile {{
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
}}
QLabel#StatValue {{ font-size: 17px; font-weight: 700; color: {TEXT}; }}
QLabel#StatName {{ font-size: 9px; letter-spacing: 1px; color: {TEXT_FAINT}; }}

/* Detected-objects list */
QLabel#CountPill {{
    color: {ACCENT};
    background-color: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 9px;
    padding: 1px 10px;
    font-weight: 600;
    font-size: 12px;
}}
QFrame#ObjRow {{
    background-color: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
}}
QLabel#ObjName {{ font-size: 13px; font-weight: 600; color: {TEXT}; }}
QLabel#ObjPct {{ font-size: 12px; color: {TEXT_DIM}; }}

/* Assistant chat */
QLineEdit#ChatInput {{
    background-color: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(120, 160, 255, 0.14);
    border-radius: 10px;
    padding: 8px 12px;
    color: {TEXT};
    font-size: 13px;
}}
QLineEdit#ChatInput:focus {{ border-color: rgba(120, 180, 255, 0.30); }}
QPushButton#ChatSend {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {ACCENT}, stop:1 {ACCENT_2});
    color: #04121e;
    border: none;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 600;
}}
QPushButton#ChatSend:hover {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4cc5fb, stop:1 #7278f2);
}}
QPushButton#ChatSend:disabled {{ background-color: rgba(255, 255, 255, 0.08); color: {TEXT_FAINT}; }}
QLabel#ChatUser {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {ACCENT}, stop:1 {ACCENT_2});
    color: #051018;
    border-radius: 12px;
    padding: 8px 11px;
    font-size: 12.5px;
}}
QLabel#ChatAI {{
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.06);
    color: {TEXT_DIM};
    border-radius: 12px;
    padding: 8px 11px;
    font-size: 12.5px;
}}

/* Scene panel */
QLabel#SceneStatus {{ font-size: 10px; letter-spacing: 1px; color: {ACCENT}; }}
QLabel#SceneChip {{
    background-color: rgba(56, 189, 248, 0.10);
    color: #cfe8ff;
    border: 1px solid rgba(56, 189, 248, 0.22);
    border-radius: 8px;
    padding: 3px 9px;
    font-size: 11px;
}}

/* Recognised text lines */
QLabel#TextLine {{
    font-size: 12px;
    color: {TEXT_DIM};
    background-color: rgba(244, 114, 182, 0.08);
    border: 1px solid rgba(244, 114, 182, 0.20);
    border-radius: 8px;
    padding: 6px 10px;
}}

/* Scrollbars */
QScrollBar:vertical {{ background: transparent; width: 8px; margin: 0; }}
QScrollBar::handle:vertical {{ background: rgba(120, 160, 255, 0.18); border-radius: 4px; min-height: 24px; }}
QScrollBar::handle:vertical:hover {{ background: rgba(120, 160, 255, 0.34); }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""


def apply_theme(app):
    """Apply the IntelliSight dark theme to a QApplication."""
    app.setStyleSheet(STYLE)
