import wx
import os
import sys
import wx.stc
from components.helpdialog import show_about_dialog

APP_NAME = "JereIDE"
DEFAULT_WINDOW_SIZE = (800, 600)
EDITOR_FONT_FACE = "Menlo"
EDITOR_FONT_SIZE = 10
LINE_NUMBER_MARGIN_ID = 1
INITIAL_MARGIN_WIDTH = 40
MARGIN_PADDING = 4
FILE_WILDCARDS = "Text files (*.txt)|*.txt|All files (*.*)|*.*"
UNTITLED_NAME = "Untitled"
MACOS_EDITED_SUFFIX = " — Edited"
OTHER_EDITED_SUFFIX = " •"
OPEN_DIALOG_TITLE = "Open file"
SAVE_DIALOG_TITLE = "Save file as"

# Menu item labels and help strings
MENU_FILE_LABEL = "&File"
MENU_OPEN_LABEL = "&Open...\tCtrl+O"
MENU_OPEN_HELP = "Open a file"
MENU_SAVE_LABEL = "&Save\tCtrl+S"
MENU_SAVE_HELP = "Save the file"

MENU_HELP_LABEL = "&Help"
MENU_ABOUT_LABEL = f"&About {APP_NAME}"
MENU_ABOUT_HELP = f"Show information about {APP_NAME}"


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        # Use wx.Size for the window dimensions to satisfy type checking.
        super(MainFrame, self).__init__(parent, title=title, size=wx.Size(*DEFAULT_WINDOW_SIZE))
        self.current_file = None
        self.is_modified = False
        self.init_ui()
        self.update_title()

    def init_ui(self):
        self.create_menu()
        self.create_text_area()
        self.Centre()
        self.Show()

    def create_menu(self):
        """Create the menu bar with keyboard shortcuts and an About dialog."""
        menu_bar = wx.MenuBar()

        # ---- File menu -------------------------------------------------
        file_menu = wx.Menu()
        open_item = file_menu.Append(
            wx.ID_OPEN, MENU_OPEN_LABEL, MENU_OPEN_HELP)
        save_item = file_menu.Append(
            wx.ID_SAVE, MENU_SAVE_LABEL, MENU_SAVE_HELP)

        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)

        menu_bar.Append(file_menu, MENU_FILE_LABEL)

        # ---- Help menu ------------------------------------------------
        help_menu = wx.Menu()
        about_item = help_menu.Append(
            wx.ID_ABOUT, MENU_ABOUT_LABEL, MENU_ABOUT_HELP)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

        menu_bar.Append(help_menu, MENU_HELP_LABEL)

        self.SetMenuBar(menu_bar)

    def create_text_area(self):
        """Create a StyledTextCtrl with line numbers using the Menlo font."""
        menlo_font = wx.Font(
            EDITOR_FONT_SIZE,
            wx.FONTFAMILY_MODERN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            EDITOR_FONT_FACE,
        )

        # StyledTextCtrl provides built‑in line numbers via a margin.
        self.text_ctrl = wx.stc.StyledTextCtrl(self, style=wx.TE_MULTILINE)
        self.text_ctrl.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, menlo_font)
        self.text_ctrl.StyleSetSize(wx.stc.STC_STYLE_DEFAULT, EDITOR_FONT_SIZE)
        self.text_ctrl.StyleClearAll()

        self.text_ctrl.SetMarginType(LINE_NUMBER_MARGIN_ID, wx.stc.STC_MARGIN_NUMBER)
        self.text_ctrl.SetMarginWidth(LINE_NUMBER_MARGIN_ID, INITIAL_MARGIN_WIDTH)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.text_ctrl.SetUseHorizontalScrollBar(False)
        self.text_ctrl.SetWrapMode(wx.stc.STC_WRAP_WORD)
        self.text_ctrl.Bind(wx.stc.EVT_STC_CHANGE, self.on_text_change)
        self.update_line_number_margin()
        self.Show()

    def update_line_number_margin(self):
        """Adjust the width of the line‑number margin so numbers never get clipped."""
        line_count = self.text_ctrl.GetLineCount()
        digit_count = len(str(line_count))
        margin_width = self.text_ctrl.TextWidth(
            wx.stc.STC_STYLE_LINENUMBER, "9" * digit_count
        ) + MARGIN_PADDING
        self.text_ctrl.SetMarginWidth(LINE_NUMBER_MARGIN_ID, margin_width)

    def on_text_change(self, event):
        # Mark document as modified when text changes
        self.is_modified = True
        self.update_title()
        self.update_line_number_margin()

        # Let the control manage its own vertical scrolling.
        if event:
            event.Skip()

    # -----------------------------------------------------------------
    # Menu command handlers
    # -----------------------------------------------------------------
    def on_open(self, event):
        dialog = wx.FileDialog(
            self, OPEN_DIALOG_TITLE, os.getcwd(), "", FILE_WILDCARDS, wx.FD_OPEN
        )
        if dialog.ShowModal() == wx.ID_OK:
            self.current_file = dialog.GetPath()
            with open(self.current_file, "r") as file:
                self.text_ctrl.SetValue(file.read())
            # Reset modification status and update title
            self.is_modified = False
            self.update_title()
            # Update the line‑number margin after loading a file.
            self.update_line_number_margin()
        dialog.Destroy()

    def on_save(self, event):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_ctrl.GetValue())
            # Reset modification status and update title
            self.is_modified = False
            self.update_title()
        else:
            dialog = wx.FileDialog(
                self,
                SAVE_DIALOG_TITLE,
                os.getcwd(),
                "",
                FILE_WILDCARDS,
                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            )
            if dialog.ShowModal() == wx.ID_OK:
                self.current_file = dialog.GetPath()
                with open(self.current_file, "w") as file:
                    file.write(self.text_ctrl.GetValue())
                # Reset modification status and update title
                self.is_modified = False
                self.update_title()
            dialog.Destroy()

    def on_about(self, event):
        """Display an About dialog for JereIDE."""
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


class MainApp(wx.App):
    def OnInit(self):
        # Title now reflects the actual application name.
        self.frame = MainFrame(None, APP_NAME)
        return True


if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()
