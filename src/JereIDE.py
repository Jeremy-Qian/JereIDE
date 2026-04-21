import wx
from constants import APP_NAME
from components.main_frame import MainFrame

class MainApp(wx.App):
    def OnInit(self):
        """Initialize the application and show the main frame."""
        self.frame = MainFrame(None, APP_NAME)
        return True

if __name__ == "__main__":
    # Create the application object
    app = MainApp()
    # Start the event loop
    app.MainLoop()
