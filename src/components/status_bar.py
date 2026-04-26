"""Status bar widget for JereIDE."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel

from components.editor import Editor
from constants import (
    INITIAL_CURSOR_POSITION_LABEL,
    STATUS_BAR_BG_COLOR,
    STATUS_BAR_BUTTON_PRESS_COLOR,
    STATUS_BAR_HEIGHT_PX,
)


class StatusBar(QWidget):
    def __init__(self, on_sidebar_toggle=None):
        """Initialize the status bar with a fixed height and line/column display."""
        super().__init__()
        self._on_sidebar_toggle_callback = on_sidebar_toggle

        self.setStyleSheet(f"background-color: {STATUS_BAR_BG_COLOR};")
        self.setFixedHeight(STATUS_BAR_HEIGHT_PX)

        self.sidebar_toggle_btn = QPushButton("◀")
        self.sidebar_toggle_btn.setFixedSize(24, STATUS_BAR_HEIGHT_PX - 2)
        self.sidebar_toggle_btn.setStyleSheet(
            f"border: none; background-color: {STATUS_BAR_BG_COLOR};"
            f"color: #666666; font-size: 12px;"
        )
        self.sidebar_toggle_btn.clicked.connect(self.on_toggle_sidebar)

        self.cursor_position_label = QLabel(INITIAL_CURSOR_POSITION_LABEL)
        self.cursor_position_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cursor_position_label.setStyleSheet(
            "border: none; padding: 0 10px; color: #666666;"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.sidebar_toggle_btn)
        layout.addWidget(self.cursor_position_label, 1)

        # Populated later via set_sidebar().
        self.sidebar: QWidget | None = None

    def update_status(self, line_number: int, column_number: int) -> None:
        """Update the label with the current line and column.

        Args:
            line_number: The current line number (1-indexed).
            column_number: The current column number (0-indexed).
        """
        self.cursor_position_label.setText(f"{line_number}:{column_number}")
        self.update()

    def update_from_editor(self, editor: Editor) -> None:
        """Extract line and column from an Editor and refresh the status.

        Args:
            editor: The Editor instance.
        """
        cursor = editor.textCursor()
        line_number = cursor.blockNumber() + 1
        column_number = cursor.columnNumber()
        self.update_status(line_number, column_number)

    def set_sidebar(self, sidebar: QWidget, on_sidebar_toggle=None) -> None:
        """Set the sidebar reference for toggling.

        Args:
            sidebar: The SideBar instance to toggle.
            on_sidebar_toggle: Optional callback to notify when sidebar is toggled.
        """
        self.sidebar = sidebar
        self._on_sidebar_toggle_callback = on_sidebar_toggle

    def on_toggle_sidebar(self) -> None:
        """Handle the sidebar toggle button click."""
        if self.sidebar is not None:
            self.sidebar.toggle_visibility()
            # Update button arrow direction
            if self.sidebar.isVisible():
                self.sidebar_toggle_btn.setText("◀")
            else:
                self.sidebar_toggle_btn.setText("▶")
            
            if self._on_sidebar_toggle_callback:
                self._on_sidebar_toggle_callback(self.sidebar.isVisible())
