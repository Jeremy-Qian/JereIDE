import os
from typing import cast

import wx
import wx.aui
import wx.stc

from components.editor import Editor
from components.help_dialog import show_about_dialog
from components.menu_builder import create_menu_bar
from components.sidebar import SideBar
from components.status_bar import StatusBar
from constants import (
    DEFAULT_WINDOW_SIZE,
    MACOS_EDITED_SUFFIX,
    UNTITLED_NAME,
)
from utils.file_io import open_file, save_file


class MainFrame(wx.Frame):
    def __init__(self, parent, title: str):
        # Use wx.Size for the window dimensions to satisfy type checking.
        super().__init__(parent, title=title, size=wx.Size(*DEFAULT_WINDOW_SIZE))
        self._init_ui()
        
        # Open an initial empty tab
        self.on_new(None)

    def _init_ui(self) -> None:
        """Initialize the UI components and layout."""
        create_menu_bar(self)

        # Initialize the Notebook for tabs
        self.notebook = wx.aui.AuiNotebook(self, style=wx.aui.AUI_NB_DEFAULT_STYLE | wx.aui.AUI_NB_CLOSE_ON_ALL_TABS)
        self.notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self._on_page_changed)
        self.notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self._on_page_close)

        self.sidebar = SideBar(self, on_sidebar_toggle=self._on_sidebar_toggled)

        self.status_bar = StatusBar(self, on_sidebar_toggle=self._on_sidebar_toggled)
        self.status_bar.set_sidebar(self.sidebar, self._on_sidebar_toggled)
        self.status_bar.sidebar_toggle_btn.Bind(
            wx.EVT_BUTTON, self.status_bar.on_toggle_sidebar
        )

        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        # Content area: sidebar on the left, separator, and notebook taking the rest.
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        content_sizer.Add(self.sidebar, 0, wx.EXPAND | wx.RIGHT, 5)
        
        # Add separator line that will be shown/hidden with the sidebar
        self.sidebar_separator = wx.StaticLine(self, style=wx.LI_VERTICAL)
        self.sidebar_separator.Hide()  # Start hidden since sidebar is hidden
        content_sizer.Add(self.sidebar_separator, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        
        content_sizer.Add(self.notebook, 1, wx.EXPAND)
        outer_sizer.Add(content_sizer, 1, wx.EXPAND)

        # Status bar pinned to the bottom, spanning full width.
        outer_sizer.Add(self.status_bar, 0, wx.EXPAND)
        self.SetSizer(outer_sizer)

        self.Centre()
        self.Show()

    def get_current_editor(self) -> Editor | None:
        """Returns the editor in the currently selected tab."""
        selection = self.notebook.GetSelection()
        if selection != wx.NOT_FOUND:
            return cast(Editor, self.notebook.GetPage(selection))
        return None

    def add_new_tab(self, path: str | None = None, content: str = "") -> None:
        """Create a new editor tab."""
        editor = Editor(self.notebook, file_path=path)
        editor.SetValue(content)
        editor.EmptyUndoBuffer()
        
        editor.Bind(wx.stc.EVT_STC_CHANGE, self._on_text_change)
        editor.Bind(wx.stc.EVT_STC_UPDATEUI, self._on_update_ui)
        
        display_name = os.path.basename(path) if path else UNTITLED_NAME
        self.notebook.AddPage(editor, display_name, select=True)
        
        editor.update_line_number_margin()
        self._update_title()

    # ------------------------------------------------------------------ events
    def _on_page_changed(self, event: wx.aui.AuiNotebookEvent) -> None:
        """Update window title and status bar when switching tabs."""
        editor = self.get_current_editor()
        if editor:
            self._update_title()
            self.status_bar.update_from_editor(editor)
        if event is not None:
            event.Skip()

    def _on_page_close(self, event: wx.aui.AuiNotebookEvent) -> None:
        """Handle tab closure, checking for unsaved changes."""
        idx = event.GetSelection()
        editor = cast(Editor, self.notebook.GetPage(idx))
        
        if editor.GetModify():
            res = wx.MessageBox(
                "File has unsaved changes. Save before closing?",
                "Unsaved Changes",
                wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION,
                self
            )
            if res == wx.YES:
                # Reuse on_save logic but for a specific editor
                self.notebook.SetSelection(idx)
                if not self._save_editor(editor):
                    event.Veto()
                    return
            elif res == wx.CANCEL:
                event.Veto()
                return
        
        # If last page is closed, we might want to open a new one or keep it empty
        # AuiNotebook handles the removal if not vetoed.

    def _on_text_change(self, event: wx.stc.StyledTextEvent) -> None:
        """Mark the buffer dirty and refresh title + line-number margin."""
        editor = cast(Editor, event.GetEventObject())
        self._update_title()

        # Update tab text to show modified indicator
        idx = self.notebook.GetPageIndex(editor)
        if idx != wx.NOT_FOUND:
            name = os.path.basename(editor.file_path) if editor.file_path else UNTITLED_NAME
            if editor.GetModify():
                name += "*"
            self.notebook.SetPageText(idx, name)

        editor.update_line_number_margin()
        if event is not None:
            event.Skip()

    def _on_update_ui(self, event: wx.stc.StyledTextEvent) -> None:
        """Refresh the status bar in response to caret/selection changes."""
        editor = cast(Editor, event.GetEventObject())
        if editor == self.get_current_editor():
            self.status_bar.update_from_editor(editor)
        if event is not None:
            event.Skip()

    def on_toggle_line_numbers(self, event: wx.CommandEvent) -> None:
        """Handle the Toggle Line Numbers menu command."""
        editor = self.get_current_editor()
        if editor:
            editor.toggle_line_numbers()

    def _on_sidebar_toggled(self, is_shown: bool) -> None:
        """Handle sidebar toggle - show/hide separator line accordingly."""
        self.sidebar_separator.Show(is_shown)
        self.Layout()

    def on_new(self, event: wx.CommandEvent | None) -> None:
        """Handle the New menu command."""
        self.add_new_tab()

    def on_open(self, event: wx.CommandEvent) -> None:
        """Handle the Open menu command."""
        opened_path, opened_content = open_file(self)
        if opened_path is None:
            return
        
        # Check if already open
        for i in range(self.notebook.GetPageCount()):
            page = cast(Editor, self.notebook.GetPage(i))
            if page.file_path == opened_path:
                self.notebook.SetSelection(i)
                return

        self.add_new_tab(opened_path, opened_content or "")

    def on_save(self, event: wx.CommandEvent) -> None:
        """Handle the Save menu command."""
        editor = self.get_current_editor()
        if editor:
            self._save_editor(editor)

    def on_save_as(self, event: wx.CommandEvent) -> None:
        """Handle the Save As menu command."""
        editor = self.get_current_editor()
        if editor:
            self._save_editor(editor, force_dialog=True)

    def on_close_tab(self, event: wx.CommandEvent) -> None:
        """Handle the Close Tab menu command."""
        selection = self.notebook.GetSelection()
        if selection != wx.NOT_FOUND:
            # This triggers EVT_AUINOTEBOOK_PAGE_CLOSE
            self.notebook.DeletePage(selection)

    def _save_editor(self, editor: Editor, force_dialog: bool = False) -> bool:
        """Internal helper to save a specific editor's content."""
        path_to_save = None if force_dialog else editor.file_path
        saved_path = save_file(self, path_to_save, editor.GetText())
        
        if not saved_path:
            return False

        editor.file_path = saved_path
        editor.SetSavePoint()
        self.notebook.SetPageText(self.notebook.GetPageIndex(editor), os.path.basename(saved_path))
        self._update_title()
        return True

    def on_about(self, event: wx.CommandEvent) -> None:
        """Display an About dialog for JereIDE."""
        show_about_dialog(self)

    # ------------------------------------------------------------------ title
    def _update_title(self) -> None:
        """Update the window title to reflect current file name and modification status."""
        editor = self.get_current_editor()
        if not editor:
            self.SetTitle(f"{UNTITLED_NAME} - {os.path.basename(os.getcwd())}")
            self.SetRepresentedFilename("")
            self.OSXSetModified(False)
            return

        path = editor.file_path
        is_modified = editor.GetModify()

        if path:
            display_title = os.path.basename(path)
            self.SetRepresentedFilename(path)
        else:
            display_title = UNTITLED_NAME
            self.SetRepresentedFilename("")

        if is_modified:
            self.OSXSetModified(True)
            display_title += MACOS_EDITED_SUFFIX
        else:
            self.OSXSetModified(False)

        self.SetTitle(display_title)