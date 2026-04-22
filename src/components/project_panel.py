import wx


class ProjectPanel(wx.Panel):
    def __init__(self, parent):
        """Initialize the project panel as a collapsible side panel."""
        super(ProjectPanel, self).__init__(parent)

        # Set a light background color
        self.SetBackgroundColour((240, 240, 240))

        # Set a default width for the side panel
        self.SetMinSize((200, -1))

        # Create the text label centered
        self.label = wx.StaticText(self, label="Needs Implementation", style=wx.ALIGN_CENTER)
        font = self.label.GetFont()
        font.PointSize = 12
        self.label.SetFont(font)

        # Layout with centered text
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()
        sizer.Add(self.label, 0, wx.ALIGN_CENTER)
        sizer.AddStretchSpacer()
        self.SetSizer(sizer)

        # Initially hidden
        self.Hide()

    def toggle_project_panel(self):
        """Toggle the visibility of the project panel."""
        if self.IsShown():
            self.Hide()
        else:
            self.Show()
        self.GetParent().Layout()