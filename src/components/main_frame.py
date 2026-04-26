"""Main window frame for JereIDE using PySide6."""

import os
from typing import cast

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QMessageBox, QWidget

from components.editor import Editor
from components.find_replace_dialog import FindDialog, ReplaceDialog
from components.help_dialog import show_about_dialog
from components.jereidebook import JereIDEBook
from components.menu import create_menu_bar
from components.sidebar import SideBar
from components.status_bar import StatusBar
from constants import (
    DEFAULT_WINDOW_SIZE,
    MACOS_EDITED_SUFFIX,
    UNTITLED_NAME,
)
from utils.file_io import open_file, save_file, FileOperationResult


class MainFrame(QMainWindow):
    def __init__(self, title: str = "JereIDE"):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(*DEFAULT_WINDOW_SIZE)
        self._init_ui()

        # Open an initial empty tab
        self.on_new()

    def _init_ui(self) -> None:
        """Initialize the UI components and layout."""
        create_menu_bar(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.notebook = JereIDEBook()
        self.sidebar = SideBar(on_sidebar_toggle=self._on_sidebar_toggled)
        self.status_bar = StatusBar(on_sidebar_toggle=self._on_sidebar_toggled)
        self.status_bar.set_sidebar(self.sidebar, self._on_sidebar_toggled)

        main_layout = QWidget()
        from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
        layout = QVBoxLayout(main_layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Content area: sidebar on the left and notebook taking the rest
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar_separator = QWidget()
        self.sidebar_separator.setFixedWidth(4)
        self.sidebar_separator.setStyleSheet("background-color: #CCCCCC;")
        self.sidebar_separator.hide()

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.sidebar_separator)
        content_layout.addWidget(self.notebook, 1)

        layout.addWidget(content_widget, 1)
        layout.addWidget(self.status_bar)

        self.setCentralWidget(main_layout)

        self.sidebar.hide()

    def get_current_editor(self) -> Editor | None:
        """Returns the editor in the currently selected tab."""
        return self.notebook.get_current_editor()

    def add_new_tab(self, path: str | None = None, content: str = "") -> None:
        """Create a new editor tab."""
        editor = Editor(file_path=path)
        editor.setText(content)
        editor.setModified(False)

        editor.textChanged.connect(self._on_text_change)
        editor.cursorPositionChanged.connect(self._on_update_ui)

        display_name = os.path.basename(path) if path else UNTITLED_NAME
        self.notebook.add_tab(display_name, editor)

        editor.update_line_number_margin()
        self._update_title()

    # ------------------------------------------------------------------ events
    def _on_text_change(self) -> None:
        """Mark the buffer dirty and refresh title + line-number margin."""
        editor = self.sender()
        if not isinstance(editor, Editor):
            return
        self._update_title()

        # Update tab text to show modified indicator
        idx = self.notebook.indexOf(editor)
        if idx >= 0:
            name = os.path.basename(editor.file_path) if editor.file_path else UNTITLED_NAME
            if editor.isModified():
                name += "*"
            self.notebook.set_tab_text(idx, name)

        editor.update_line_number_margin()

    def _on_update_ui(self) -> None:
        """Refresh the status bar in response to caret/selection changes."""
        editor = self.get_current_editor()
        if editor:
            self.status_bar.update_from_editor(editor)

    def _on_sidebar_toggled(self, is_shown: bool) -> None:
        """Handle sidebar toggle - show/hide separator line accordingly."""
        self.sidebar_separator.setVisible(is_shown)
        self.update()

    def on_toggle_line_numbers(self) -> None:
        """Handle the Toggle Line Numbers menu command."""
        editor = self.get_current_editor()
        if editor:
            editor.toggle_line_numbers()

    def on_new(self) -> None:
        """Handle the New menu command."""
        self.add_new_tab()

    def on_open(self) -> None:
        """Handle the Open menu command."""
        result = open_file(self)
        if not result.success:
            return
        if result.path is None:
            return

        # Check if already open
        for i in range(self.notebook.count()):
            page = self.notebook.widget(i)
            if isinstance(page, Editor) and page.file_path == result.path:
                self.notebook.setCurrentIndex(i)
                return

        self.add_new_tab(result.path, result.content or "")

    def on_save(self) -> None:
        """Handle the Save menu command."""
        editor = self.get_current_editor()
        if editor:
            self._save_editor(editor)

    def on_save_as(self) -> None:
        """Handle the Save As menu command."""
        editor = self.get_current_editor()
        if editor:
            self._save_editor(editor, force_dialog=True)

    def on_close_tab(self) -> None:
        """Handle the Close Tab menu command."""
        idx = self.notebook.currentIndex()
        if idx >= 0:
            self._close_tab_by_index(idx)

    def _close_tab_by_index(self, idx: int) -> bool:
        """Internal method to close a tab by index, checking for unsaved changes."""
        editor = self.notebook.widget(idx)
        if isinstance(editor, Editor) and editor.isModified():
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "File has unsaved changes. Save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self.notebook.setCurrentIndex(idx)
                if not self._save_editor(editor):
                    return False
            elif reply == QMessageBox.Cancel:
                return False

        self.notebook.removeTab(idx)
        return True

    # ------------------------------------------------------------------ Find/Replace
    def on_find(self) -> None:
        """Handle the Find menu command (Ctrl+F)."""
        editor = self.get_current_editor()
        if editor:
            dialog = FindDialog(self, editor)
            dialog.show()

    def on_find_next(self) -> None:
        """Handle the Find Next menu command (F3)."""
        editor = self.get_current_editor()
        if editor:
            selected_text = editor.selectedText()
            if selected_text:
                editor.findNext(selected_text, 0)

    def on_replace(self) -> None:
        """Handle the Replace menu command (Ctrl+H)."""
        editor = self.get_current_editor()
        if editor:
            dialog = ReplaceDialog(self, editor)
            dialog.show()

    # ------------------------------------------------------------------ save
    def _save_editor(self, editor: Editor, force_dialog: bool = False) -> bool:
        """Internal helper to save a specific editor's content."""
        path_to_save = None if force_dialog else editor.file_path
        result = save_file(self, path_to_save, editor.text())

        if not result.success:
            return False

        editor.file_path = result.path
        editor.setModified(False)
        idx = self.notebook.indexOf(editor)
        if idx >= 0:
            self.notebook.set_tab_text(idx, os.path.basename(result.path or ""))
        self._update_title()
        return True

    def on_about(self) -> None:
        """Display an About dialog for JereIDE."""
        show_about_dialog(self)

    # ------------------------------------------------------------------ title
    def _update_title(self) -> None:
        """Update the window title to reflect current file name and modification status."""
        editor = self.get_current_editor()
        if not editor:
            self.setWindowTitle(f"{UNTITLED_NAME} - {os.path.basename(os.getcwd())}")
            return

        path = editor.file_path
        is_modified = editor.isModified()

        if path:
            display_title = os.path.basename(path)
        else:
            display_title = UNTITLED_NAME

        if is_modified:
            display_title += MACOS_EDITED_SUFFIX

        self.setWindowTitle(display_title)
