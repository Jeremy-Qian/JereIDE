import wx
import sys
import os
import wx.stc
from constants import *
from components.editor import Editor
from components.status_bar import StatusPanel
from components.menu_builder import create_menu_bar
from utils.file_io import open_file, save_file

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        # Use wx.Size for the window dimensions to satisfy type checking.
        super(MainFrame, self).__init__(parent, title=title, size=wx.Size(*DEFAULT_WINDOW_SIZE))
        self.current_file = None
        self.is_modified = False
        self.init_ui()
        self.update_title()

    def init_ui(self):
        """Initialize the UI components and layout."""
        # Setup Menu
        create_menu_bar(self)

        # Setup Editor Component
        self.editor = Editor(self)
        self.editor.Bind(wx.stc.EVT_STC_CHANGE, self.on_text_change)
        self.editor.Bind(wx.stc.EVT_STC_UPDATEUI, self.on_update_ui)

        # Setup Status Panel (replacing traditional status bar)
        self.status_panel = StatusPanel(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.editor, 1, wx.EXPAND)
        sizer.Add(self.status_panel, 0, wx.EXPAND)
        self.SetSizer(sizer)

        self.Centre()
        self.Show()

    def on_text_change(self, event):
        """Handle text change events in the editor."""
        self.is_modified = True
        self.update_title()
        self.editor.update_line_number_margin()
        if event:
            event.Skip()

    def on_update_ui(self, event):
        """Handle UI update events to refresh the status panel."""
        self.status_panel.update_from_editor(self.editor)
        if event:
            event.Skip()

    def on_toggle_line_numbers(self, event):
        """Handle the Toggle Line Numbers menu command."""
        self.editor.toggle_line_numbers()

    def on_open(self, event):
        """Handle the Open menu command."""
        path, content = open_file(self)
        if path is not None:
            self.current_file = path
            self.editor.SetValue(content)
            # Reset modification status and update title
            self.is_modified = False
            self.update_title()
            # Update the line‑number margin after loading a file.
            self.editor.update_line_number_margin()
            # Update the status panel.
            self.status_panel.update_from_editor(self.editor)

    def on_save(self, event):
        """Handle the Save menu command."""
        content = self.editor.GetValue()
        path = save_file(self, self.current_file, content)
        if path:
            self.current_file = path
            # Reset modification status and update title
            self.is_modified = False
            self.update_title()

    def on_about(self, event):
        """Display an About dialog for JereIDE."""
        from components.helpdialog import show_about_dialog
        show_about_dialog(self)

    def update_title(self):
        """Update the window title to reflect file name and modification status."""
        is_macos = sys.platform == "darwin"

        if self.current_file:
            # Extract just the filename from the full path
            file_name = os.path.basename(self.current_file)
            title = file_name
            if is_macos:
                # Set the proxy icon and path for macOS
                self.SetRepresentedFilename(self.current_file)
        else:
            title = UNTITLED_NAME
            if is_macos:
                # Clear the proxy icon for unsaved files
                self.SetRepresentedFilename("")

        # Handle modification status
        if self.is_modified:
            if is_macos:
                # Use the native macOS "dirty" state indicator (dot in the close button)
                self.OSXSetModified(True)
                # Add "- Edited" suffix for macOS
                title += MACOS_EDITED_SUFFIX
            else:
                # Add a dot to indicate unsaved changes for other platforms
                title += OTHER_EDITED_SUFFIX
        elif is_macos:
            self.OSXSetModified(False)

        # Set the window title
        self.SetTitle(title)
