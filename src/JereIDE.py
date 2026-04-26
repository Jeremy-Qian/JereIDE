"""Application entry point for JereIDE using PySide6."""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from components.main_frame import MainFrame
from constants import APP_NAME


def main():
    """Initialize and run the JereIDE application."""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    
    main_frame = MainFrame()
    main_frame.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
