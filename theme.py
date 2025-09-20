LIGHT_THEME = """
QMainWindow {
    background-color: #ffffff;
    color: #000000;
}
QWidget {
    background-color: #ffffff;
    color: #000000;
}
QGroupBox {
    font-weight: bold;
    border: 2px solid #cccccc;
    border-radius: 5px;
    margin-top: 1ex;
    padding-top: 10px;
    background-color: #ffffff;
    color: #000000;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #000000;
}
QPushButton {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 11px;
    background-color: #ffffff;
    color: #000000;
}
QPushButton:hover {
    background-color: #e0e0e0;
    color: #000000;
}
QLineEdit, QComboBox {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 6px;
    font-size: 11px;
    background-color: #ffffff;
    color: #000000;
}
QTextEdit {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #ccc;
    border-radius: 4px;
}
QTabWidget::pane {
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #ffffff;
}
QTabBar::tab {
    background-color: #e0e0e0;
    border: 1px solid #ccc;
    border-bottom: none;
    border-radius: 4px 4px 0px 0px;
    padding: 8px 16px;
    margin-right: 2px;
    color: #000000;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    border-bottom: 1px solid #ffffff;
    color: #000000;
}
QCheckBox {
    background-color: #ffffff;
    color: #000000;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #777;
    border-radius: 3px;
    background: #fff;
}
QCheckBox::indicator:checked {
    image: url(:/qt-project.org/styles/commonstyle/images/checkboxindicator.png);
}
QLabel {
    background-color: #ffffff;
    color: #000000;
}
QProgressBar {
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #ffffff;
    color: #000000;
}
QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 4px;
}
"""

DARK_THEME = """
QMainWindow {
    background-color: #2b2b2b;
    color: #e0e0e0;
}
QWidget {
    background-color: #2b2b2b;
    color: #e0e0e0;
}
QGroupBox {
    font-weight: bold;
    border: 2px solid #444444;
    border-radius: 5px;
    margin-top: 1ex;
    padding-top: 10px;
    background-color: #2f2f2f;
    color: #e0e0e0;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #f0f0f0;
}
QPushButton {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 11px;
    background-color: #3c3c3c;
    color: #ffffff;
}
QPushButton:hover {
    background-color: #505050;
    color: #ffffff;
}
QLineEdit, QComboBox {
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 6px;
    font-size: 11px;
    background-color: #3c3c3c;
    color: #ffffff;
}
QTextEdit {
    background-color: #3c3c3c;
    color: #ffffff;
    border: 1px solid #555555;
    border-radius: 4px;
}
QTabWidget::pane {
    border: 1px solid #555555;
    border-radius: 4px;
    background-color: #2f2f2f;
}
QTabBar::tab {
    background-color: #444444;
    border: 1px solid #555555;
    border-bottom: none;
    border-radius: 4px 4px 0px 0px;
    padding: 8px 16px;
    margin-right: 2px;
    color: #dddddd;
}
QTabBar::tab:selected {
    background-color: #2f2f2f;
    border-bottom: 1px solid #2f2f2f;
    color: #ffffff;
}
QCheckBox {
    background-color: transparent;
    color: #e0e0e0;
}
QLabel {
    background-color: transparent;
    color: #e0e0e0;
}
QProgressBar {
    border: 1px solid #555555;
    border-radius: 4px;
    background-color: #3c3c3c;
    color: #ffffff;
}
QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 4px;
}
"""

# default to dark btw, change it here
def apply_theme(window, theme="dark"):
    """Apply theme to the application window"""
    if theme == "light":
        window.setStyleSheet(LIGHT_THEME)
    elif theme == "dark":
        window.setStyleSheet(DARK_THEME)
    else:
        window.setStyleSheet(DARK_THEME)


def get_available_themes():
    """Get list of available themes"""
    return ["light", "dark"]


def get_button_style(button_type="default"):
    """Get specific button styles"""
    styles = {
        "success": "QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }",
        "danger": "QPushButton { background-color: #f44336; color: white; font-weight: bold; }",
        "info": "QPushButton { background-color: #2196F3; color: white; font-weight: bold; }",
        "warning": "QPushButton { background-color: #ff9800; color: white; font-weight: bold; }",
        "default": ""
    }
    return styles.get(button_type, styles["default"])