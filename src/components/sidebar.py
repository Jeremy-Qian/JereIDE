"""Sidebar widget for JereIDE."""

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy

from constants import (
    BUTTON_ICON_HEIGHT_PX,
    BUTTON_ICON_WIDTH_PX,
    GIT_ICON_FILENAME,
    ICONS_DIR_NAME,
    PROJECT_ICON_FILENAME,
    SEARCH_ICON_FILENAME,
    SIDEBAR_BG_COLOR,
    SIDEBAR_MIN_WIDTH_PX,
    SIDEBAR_PLACEHOLDER_FONT_SIZE,
    SIDEBAR_PLACEHOLDER_TEXT,
)


def _load_button_icon(icon_filename: str) -> QIcon:
    """Load and return a button icon."""
    icon_path = os.path.join(ICONS_DIR_NAME, icon_filename)
    return QIcon(icon_path)


class SideBar(QWidget):
    def __init__(self, on_sidebar_toggle=None):
        """Initialize the sidebar as two stacked panels:
        - Top panel with two horizontally arranged action buttons
        - Bottom panel containing a placeholder label (unchanged)
        The top panel has a fixed height (driven by its content), and the bottom
        panel expands to fill the remaining space.
        """
        super().__init__()
        self.on_sidebar_toggle = on_sidebar_toggle
        
        self.setBackgroundRole(QWidget().backgroundRole())
        self.setStyleSheet(f"background-color: {SIDEBAR_BG_COLOR};")
        self.setMinimumWidth(SIDEBAR_MIN_WIDTH_PX)
        self.setMaximumWidth(SIDEBAR_MIN_WIDTH_PX)

        # Top panel with action buttons
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(10, 5, 10, 5)
        
        btn_project = QPushButton()
        btn_git = QPushButton()
        btn_search = QPushButton()
        
        try:
            project_icon = _load_button_icon(PROJECT_ICON_FILENAME)
            git_icon = _load_button_icon(GIT_ICON_FILENAME)
            search_icon = _load_button_icon(SEARCH_ICON_FILENAME)
            btn_project.setIcon(project_icon)
            btn_git.setIcon(git_icon)
            btn_search.setIcon(search_icon)
        except Exception:
            # Fallback if icons are not available
            btn_project.setText("📁")
            btn_git.setText("⎇")
            btn_search.setText("🔍")
        
        btn_project.setFixedSize(24, 24)
        btn_git.setFixedSize(24, 24)
        btn_search.setFixedSize(24, 24)
        btn_project.setStyleSheet("border: none;")
        btn_git.setStyleSheet("border: none;")
        btn_search.setStyleSheet("border: none;")
        
        btn_project.clicked.connect(self._on_project)
        btn_git.clicked.connect(self._on_git)
        btn_search.clicked.connect(self._on_search)
        
        top_layout.addStretch()
        top_layout.addWidget(btn_project)
        top_layout.addWidget(btn_git)
        top_layout.addWidget(btn_search)
        top_layout.addStretch()

        # Bottom panel with placeholder text
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        placeholder = QLabel(SIDEBAR_PLACEHOLDER_TEXT)
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet(f"color: gray; font-size: {SIDEBAR_PLACEHOLDER_FONT_SIZE}px;")
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(placeholder)
        bottom_layout.addStretch()

        # Separator between top and bottom panels
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #CCCCCC;")

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(top_widget)
        main_layout.addWidget(separator)
        main_layout.addWidget(bottom_widget, 1)

        # Start collapsed
        self.hide()

    def toggle_visibility(self) -> None:
        """Toggle whether the panel is shown and re-layout the parent frame."""
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self.parent().update() if self.parent() else None
        
        if self.on_sidebar_toggle:
            self.on_sidebar_toggle(self.isVisible())

    def _on_project(self) -> None:
        """Placeholder action for the Project button."""
        pass

    def _on_search(self) -> None:
        """Handle the Search button click."""
        # Emit a signal or call the main window's search action
        pass

    def _on_git(self) -> None:
        """Placeholder action for the Git button."""
        pass
