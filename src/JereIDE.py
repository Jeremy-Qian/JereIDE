import wx
import wx.adv
import os
import sys
import wx.stc

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        # Use wx.Size for the window dimensions to satisfy type checking.
        super(MainFrame, self).__init__(parent, title=title, size=wx.Size(800, 600))
        self.current_file = None
        self.init_ui()

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
            wx.ID_OPEN, "&Open\tCtrl+O", "Open a file")
        save_item = file_menu.Append(
            wx.ID_SAVE, "&Save\tCtrl+S", "Save the file")
        exit_item = file_menu.Append(
            wx.ID_EXIT, "E&xit\tCtrl+Q", "Exit the application")

        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        menu_bar.Append(file_menu, "&File")

        # ---- Help menu ------------------------------------------------
        help_menu = wx.Menu()
        about_item = help_menu.Append(
            wx.ID_ABOUT, "&About JereIDE", "Show information about JereIDE")
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

    def create_text_area(self):
        """Create a StyledTextCtrl with line numbers using the Menlo font."""
        menlo_font = wx.Font(
            10,
            wx.FONTFAMILY_MODERN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            "Menlo",
        )

        # StyledTextCtrl provides built‑in line numbers via a margin.
        self.text_ctrl = wx.stc.StyledTextCtrl(self, style=wx.TE_MULTILINE)
        self.text_ctrl.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, menlo_font)
        self.text_ctrl.StyleSetSize(wx.stc.STC_STYLE_DEFAULT, 10)
        self.text_ctrl.StyleClearAll()

        LINE_NUMBER_MARGIN = 1
        self.text_ctrl.SetMarginType(LINE_NUMBER_MARGIN, wx.stc.STC_MARGIN_NUMBER)
        self.text_ctrl.SetMarginWidth(LINE_NUMBER_MARGIN, 40)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.text_ctrl.SetUseHorizontalScrollBar(False)
        self.text_ctrl.SetWrapMode(wx.stc.STC_WRAP_WORD)
        self.text_ctrl.Bind(wx.stc.EVT_STC_CHANGE, self.on_text_change)
        self.Show()

    def on_text_change(self, event):
        # Adjust the width of the line‑number margin so numbers never get clipped.
        line_count = self.text_ctrl.GetLineCount()
        digit_count = len(str(line_count))
        margin_width = self.text_ctrl.TextWidth(
            wx.stc.STC_STYLE_LINENUMBER, "9" * digit_count
        ) + 4
        self.text_ctrl.SetMarginWidth(1, margin_width)

        # Let the control manage its own vertical scrolling.
        if event:
            event.Skip()

    # -----------------------------------------------------------------
    # Menu command handlers
    # -----------------------------------------------------------------
    def on_open(self, event):
        wildcard = "Text files (*.txt)|*.txt|All files (*.*)|*.*"
        dialog = wx.FileDialog(
            self, "Open file", os.getcwd(), "", wildcard, wx.FD_OPEN
        )
        if dialog.ShowModal() == wx.ID_OK:
            self.current_file = dialog.GetPath()
            with open(self.current_file, "r") as file:
                self.text_ctrl.SetValue(file.read())
            # Update the line‑number margin after loading a file.
            self.on_text_change(None)
        dialog.Destroy()

    def on_save(self, event):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_ctrl.GetValue())
        else:
            wildcard = "Text files (*.txt)|*.txt|All files (*.*)|*.*"
            dialog = wx.FileDialog(
                self,
                "Save file as",
                os.getcwd(),
                "",
                wildcard,
                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            )
            if dialog.ShowModal() == wx.ID_OK:
                self.current_file = dialog.GetPath()
                with open(self.current_file, "w") as file:
                    file.write(self.text_ctrl.GetValue())
            dialog.Destroy()

    def on_exit(self, event):
        self.Close()

    def on_about(self, event):
        """Display an About dialog for JereIDE."""
        info = wx.adv.AboutDialogInfo()
        info.SetName("JereIDE")
        info.SetVersion("1.0")
        info.SetDescription(
            "JereIDE – a minimal IDE built with wxPython.\n"
            "Features include opening, saving, and basic text editing."
        )
        info.SetCopyright("(C) 2024 Jeremy")
        wx.adv.AboutBox(info)


class MainApp(wx.App):
    def OnInit(self):
        # Title now reflects the actual application name.
        self.frame = MainFrame(None, "JereIDE")
        return True


if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()
