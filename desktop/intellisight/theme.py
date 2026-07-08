"""Minimal, camera-first dark theme for IntelliSight (Qt Style Sheets).

The video fills the window; everything else is a translucent 'glass' overlay
floating on top of it. Only the color constants below are usable inside the
f-string's {braces} — every other color is a literal rgba().
"""

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

/* The camera stage fills the window; the video sits edge-to-edge. */
QFrame#Stage {{
    background-color: #04060c;
    border: 1px solid rgba(120, 160, 255, 0.12);
    border-radius: 18px;
}}
QLabel#VideoLabel {{ background-color: #04060c; border-radius: 17px; }}

/* ── Idle / start screen ── */
QLabel#StartTitle {{ font-size: 26px; font-weight: 700; color: #ffffff; }}
QLabel#StartHint {{ color: {TEXT_DIM}; font-size: 14px; }}
QLabel#ErrorText {{ color: {DANGER}; font-size: 13px; }}
QLabel#ErrorTitle {{ font-size: 22px; font-weight: 700; color: #ffffff; }}
QLabel#ErrorIcon {{ font-size: 40px; }}

QPushButton#StartBtn {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {ACCENT}, stop:1 {ACCENT_2});
    color: #04121e;
    border: none;
    border-radius: 13px;
    padding: 13px 30px;
    font-size: 14px;
    font-weight: 700;
}}
QPushButton#StartBtn:hover {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4cc5fb, stop:1 #7278f2);
}}

/* ── Floating brand (top-left) ── */
QFrame#BrandOverlay {{
    background-color: rgba(8, 12, 20, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 14px;
}}
QLabel#BrandName {{ color: #ffffff; font-size: 15px; font-weight: 700; letter-spacing: 0.3px; }}

/* ── Floating status pill (top-right) ── */
QLabel#LiveOverlay {{
    background-color: rgba(8, 12, 20, 0.55);
    border: 1px solid rgba(52, 211, 153, 0.40);
    color: {OK};
    border-radius: 13px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}}
QLabel#LiveOverlay[state="connecting"] {{
    border: 1px solid rgba(251, 191, 36, 0.40);
    color: {WARN};
}}

/* ── Floating 'Detected' card (top-right) ── */
QFrame#ObjOverlay {{
    background-color: rgba(8, 12, 20, 0.62);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 16px;
}}
QLabel#ObjTitle {{ color: {TEXT_DIM}; font-size: 10px; letter-spacing: 2.5px; font-weight: 700; }}
QLabel#ObjCount {{
    color: {ACCENT};
    background-color: rgba(56, 189, 248, 0.14);
    border-radius: 8px;
    padding: 1px 9px;
    font-size: 12px;
    font-weight: 700;
    font-family: "Menlo", "SF Mono", monospace;
}}
QLabel#ObjRowName {{ color: {TEXT}; font-size: 13px; font-weight: 600; }}
QLabel#ObjRowPct {{
    color: {TEXT_DIM};
    font-size: 11px;
    font-weight: 600;
    font-family: "Menlo", "SF Mono", monospace;
}}
QLabel#ObjEmpty {{ color: {TEXT_FAINT}; font-size: 12px; }}

/* ── Floating stop button (bottom-center) ── */
QPushButton#StopFloat {{
    background-color: rgba(8, 12, 20, 0.62);
    border: 1px solid rgba(248, 113, 113, 0.42);
    color: {DANGER};
    border-radius: 14px;
    padding: 11px 26px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}
QPushButton#StopFloat:hover {{ background-color: rgba(248, 113, 113, 0.20); }}
"""


def apply_theme(app):
    """Apply the IntelliSight dark theme to a QApplication."""
    app.setStyleSheet(STYLE)
