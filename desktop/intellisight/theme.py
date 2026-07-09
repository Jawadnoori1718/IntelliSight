"""Minimal, camera-first dark theme for Big Brother (Qt Style Sheets).

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

/* ── Activity feed (top-left) ── */
QFrame#EventFeed {{
    background-color: rgba(8, 12, 20, 0.62);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 16px;
}}
QLabel#EventTitle {{ color: {TEXT_DIM}; font-size: 10px; letter-spacing: 2.5px; font-weight: 700; }}
QLabel#EventText {{ color: {TEXT}; font-size: 12.5px; font-weight: 500; }}
QLabel#EventTime {{ color: {TEXT_FAINT}; font-size: 10px; font-family: "Menlo", "SF Mono", monospace; }}
QLabel#EventEmpty {{ color: {TEXT_FAINT}; font-size: 12px; }}

/* ── Floating control bar (bottom-center): Rules · Timeline · Stop ── */
QFrame#ControlBar {{
    background-color: rgba(8, 12, 20, 0.70);
    border: 1px solid rgba(255, 255, 255, 0.11);
    border-radius: 16px;
}}
QFrame#BarSep {{ background-color: rgba(255, 255, 255, 0.09); }}
QPushButton#BarBtn {{
    background: transparent;
    border: none;
    color: #dbe4f5;
    border-radius: 11px;
    padding: 9px 17px;
    font-size: 13px;
    font-weight: 600;
}}
QPushButton#BarBtn:hover {{ background-color: rgba(255, 255, 255, 0.08); color: #ffffff; }}
QPushButton#BarStop {{
    background: transparent;
    border: none;
    color: {DANGER};
    border-radius: 11px;
    padding: 9px 17px;
    font-size: 13px;
    font-weight: 700;
}}
QPushButton#BarStop:hover {{ background-color: rgba(248, 113, 113, 0.16); }}

/* ── Counting zone controls (bottom-center) ── */
QLabel#ZoneHint {{
    background-color: rgba(8, 12, 20, 0.55);
    border: 1px solid rgba(251, 191, 36, 0.30);
    color: {WARN};
    border-radius: 12px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
}}
QPushButton#ZoneClear {{
    background-color: rgba(8, 12, 20, 0.62);
    border: 1px solid rgba(251, 191, 36, 0.42);
    color: {WARN};
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}
QPushButton#ZoneClear:hover {{ background-color: rgba(251, 191, 36, 0.18); }}

/* ── Rules button (bottom-left) + toast ── */
QPushButton#RulesButton {{
    background-color: rgba(8, 12, 20, 0.62);
    border: 1px solid rgba(129, 140, 248, 0.45);
    color: #a5b4fc;
    border-radius: 14px;
    padding: 11px 20px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}
QPushButton#RulesButton:hover {{ background-color: rgba(129, 140, 248, 0.18); }}
QPushButton#TimelineButton {{
    background-color: rgba(8, 12, 20, 0.62);
    border: 1px solid rgba(56, 189, 248, 0.42);
    color: #7dd3fc;
    border-radius: 14px;
    padding: 11px 20px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}
QPushButton#TimelineButton:hover {{ background-color: rgba(56, 189, 248, 0.16); }}
QLabel#Toast {{
    background-color: rgba(99, 102, 241, 0.92);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 14px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 700;
}}

/* ── Rules + Timeline dialogs ── */
QDialog#RulesDialog, QDialog#TimelineDialog {{ background-color: {BG}; }}
QLabel#RulesHeader {{ font-size: 21px; font-weight: 700; color: #ffffff; }}
QLabel#RulesSub {{ color: {TEXT_DIM}; font-size: 13px; }}
QLabel#RuleWord {{ color: {TEXT_DIM}; font-size: 13px; font-weight: 700; }}
QFrame#RuleItem {{
    background-color: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 10px;
}}
QLabel#RuleDesc {{ color: {TEXT}; font-size: 13px; }}
QLabel#RulesEmpty {{ color: {TEXT_FAINT}; font-size: 13px; }}
QComboBox, QSpinBox {{
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(120, 160, 255, 0.18);
    border-radius: 9px;
    padding: 7px 10px;
    color: {TEXT};
    min-height: 18px;
}}
QComboBox:focus, QSpinBox:focus {{ border-color: rgba(120, 180, 255, 0.42); }}
QComboBox::drop-down {{ border: none; width: 20px; }}
QComboBox QAbstractItemView {{
    background-color: #0b1220;
    color: {TEXT};
    selection-background-color: rgba(56, 189, 248, 0.30);
    border: 1px solid rgba(120, 160, 255, 0.20);
    outline: none;
}}
QPushButton#AddRuleBtn {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {ACCENT}, stop:1 {ACCENT_2});
    color: #04121e;
    border: none;
    border-radius: 10px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 700;
}}
QPushButton#AddRuleBtn:hover {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4cc5fb, stop:1 #7278f2);
}}
QPushButton#RemoveRuleBtn {{
    background-color: transparent;
    color: {TEXT_DIM};
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 12px;
}}
QPushButton#RemoveRuleBtn:hover {{ color: {DANGER}; border-color: rgba(248, 113, 113, 0.40); }}
QCheckBox {{ color: {TEXT}; spacing: 8px; }}
QCheckBox::indicator {{
    width: 18px; height: 18px;
    border-radius: 5px;
    border: 1px solid rgba(255, 255, 255, 0.25);
    background: rgba(255, 255, 255, 0.04);
}}
QCheckBox::indicator:checked {{ background-color: {ACCENT}; border-color: {ACCENT}; }}
QLineEdit {{
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(120, 160, 255, 0.18);
    border-radius: 9px;
    padding: 7px 10px;
    color: {TEXT};
}}
QLineEdit:focus {{ border-color: rgba(120, 180, 255, 0.42); }}
QLabel#SettingsTitle {{ color: {TEXT_FAINT}; font-size: 10px; letter-spacing: 2px; font-weight: 700; }}
QLabel#SettingsHelp {{ color: {TEXT_FAINT}; font-size: 11px; }}
QPushButton#SmallBtn {{
    background-color: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(120, 160, 255, 0.20);
    border-radius: 8px;
    padding: 7px 16px;
    color: {TEXT_DIM};
    font-size: 12px;
    font-weight: 600;
}}
QPushButton#SmallBtn:hover {{ border-color: rgba(120, 180, 255, 0.40); color: {TEXT}; }}
"""


def apply_theme(app):
    """Apply the Big Brother dark theme to a QApplication."""
    app.setStyleSheet(STYLE)
