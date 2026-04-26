"""About dialog for JereIDE."""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from constants import APP_COPYRIGHT, APP_DESCRIPTION, APP_NAME, APP_VERSION


def show_about_dialog(parent) -> None:
    """Display an About dialog for JereIDE."""
    dialog = QDialog(parent)
    dialog.setWindowTitle(f"About {APP_NAME}")
    dialog.setFixedSize(400, 200)
    
    layout = QVBoxLayout(dialog)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    name_label = QLabel(f"<h1>{APP_NAME}</h1>")
    name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(name_label)
    
    version_label = QLabel(f"Version {APP_VERSION}")
    version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(version_label)
    
    description_label = QLabel(f"<p>{APP_DESCRIPTION}</p>")
    description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    description_label.setWordWrap(True)
    layout.addWidget(description_label)
    
    copyright_label = QLabel(APP_COPYRIGHT)
    copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(copyright_label)
    
    close_btn = QLabel("<p><i>Built with PySide6</i></p>")
    close_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(close_btn)
    
    dialog.exec()
