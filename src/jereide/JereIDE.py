import wx
import wx.adv
import os
import sys

# Fix working directory for macOS app bundle
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
aijsofjsoidfjosadofjo

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
        """Create a multiline text control with a fixed‑width font."""
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        # Use proper font constants.
        font = wx.Font(
            10,
            wx.FONTFAMILY_MODERN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            "Menlo"
        )
        self.text_ctrl.SetFont(font)
        self.Show()

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
