import os
import sys

import wx
import wx.stc

from components.editor import Editor
from components.help_dialog import show_about_dialog
from components.menu_builder import create_menu_bar
from components.project_panel import ProjectPanel
from components.status_panel import StatusPanel
from constants import (
    DEFAULT_WINDOW_SIZE,
    MACOS_EDITED_SUFFIX,
    OTHER_EDITED_SUFFIX,
    UNTITLED_NAME,
)
from utils.file_io import open_file, save_file


class MainFrame(wx.Frame):
    def __init__(self, parent, title: str):
        # Use wx.Size for the window dimensions to satisfy type checking.
        super().__init__(parent, title=title, size=wx.Size(*DEFAULT_WINDOW_SIZE))
        self.current_file_path: str | None = None
        self.has_unsaved_changes = False
        self._init_ui()
        self._update_title()

    def _init_ui(self) -> None:
        """Initialize the UI components and layout."""
        create_menu_bar(self)

        self.editor = Editor(self)
        self.editor.Bind(wx.stc.EVT_STC_CHANGE, self._on_text_change)
        self.editor.Bind(wx.stc.EVT_STC_UPDATEUI, self._on_update_ui)

        self.project_panel = ProjectPanel(self)

        self.status_panel = StatusPanel(self)
        self.status_panel.set_project_panel(self.project_panel)
        self.status_panel.toggle_project_btn.Bind(
            wx.EVT_BUTTON, self.status_panel.on_toggle_project_panel
        )

        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        # Content area: project panel on the left, editor taking the rest.
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        content_sizer.Add(self.project_panel, 0, wx.EXPAND | wx.RIGHT, 5)
        content_sizer.Add(self.editor, 1, wx.EXPAND)
        outer_sizer.Add(content_sizer, 1, wx.EXPAND)

        # Status bar pinned to the bottom, spanning full width.
        outer_sizer.Add(self.status_panel, 0, wx.EXPAND)
        self.SetSizer(outer_sizer)

        self.Centre()
        self.Show()

    # ------------------------------------------------------------------ events
    def _on_text_change(self, event: wx.Event) -> None:
        """Mark the buffer dirty and refresh title + line-number margin."""
        self.has_unsaved_changes = True
        self._update_title()
        self.editor.update_line_number_margin()
        if event is not None:
            event.Skip()

    def _on_update_ui(self, event: wx.Event) -> None:
        """Refresh the status panel in response to caret/selection changes."""
        self.status_panel.update_from_editor(self.editor)
        if event is not None:
            event.Skip()

    def on_toggle_line_numbers(self, event: wx.CommandEvent) -> None:
        """Handle the Toggle Line Numbers menu command."""
        self.editor.toggle_line_numbers()

    def on_open(self, event: wx.CommandEvent) -> None:
        """Handle the Open menu command."""
        opened_path, opened_content = open_file(self)
        if opened_path is None:
            return

        self.current_file_path = opened_path
        self.editor.SetValue(opened_content or "")
        self.has_unsaved_changes = False
        self._update_title()
        self.editor.update_line_number_margin()
        self.status_panel.update_from_editor(self.editor)

    def on_save(self, event: wx.CommandEvent) -> None:
        """Handle the Save menu command."""
        saved_path = save_file(self, self.current_file_path, self.editor.GetValue())
        if not saved_path:
            return

        self.current_file_path = saved_path
        self.has_unsaved_changes = False
        self._update_title()

    def on_about(self, event: wx.CommandEvent) -> None:
        """Display an About dialog for JereIDE."""
        show_about_dialog(self)

    # ------------------------------------------------------------------ title
    def _update_title(self) -> None:
        """Update the window title to reflect file name and modification status."""
        is_macos = sys.platform == "darwin"

        if self.current_file_path:
            display_title = os.path.basename(self.current_file_path)
            if is_macos:
                self.SetRepresentedFilename(self.current_file_path)
        else:
            display_title = UNTITLED_NAME
            if is_macos:
                self.SetRepresentedFilename("")

        if self.has_unsaved_changes:
            if is_macos:
                # Use the native macOS "dirty" indicator (dot in the close button).
                self.OSXSetModified(True)
                display_title += MACOS_EDITED_SUFFIX
            else:
                display_title += OTHER_EDITED_SUFFIX
        elif is_macos:
            self.OSXSetModified(False)

        self.SetTitle(display_title)
