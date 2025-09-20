import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from app import YtDlpGUI

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("yt-dlp GUI")
    app.setApplicationVersion("1.0.0")
    
    # Set application icon if available
    icon_path = Path(__file__).parent / "assets" / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Create and show main window
    window = YtDlpGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()