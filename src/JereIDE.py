import wx

from components.main_frame import MainFrame
from constants import APP_NAME


class JereIDEApp(wx.App):
    def OnInit(self) -> bool:
        """Initialize the application and show the main frame."""
        self.main_frame = MainFrame(parent=None, title=APP_NAME)
        return True


if __name__ == "__main__":
    app = JereIDEApp()
    app.MainLoop()
