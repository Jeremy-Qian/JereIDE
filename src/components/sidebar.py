import wx

from constants import (
    SIDEBAR_BG_COLOR,
    SIDEBAR_MIN_WIDTH_PX,
    SIDEBAR_PLACEHOLDER_FONT_SIZE,
    SIDEBAR_PLACEHOLDER_TEXT,
)


class SideBar(wx.Panel):
    def __init__(self, parent, on_toggle_callback=None):
        """Initialize the sidebar as a collapsible side panel."""
        super().__init__(parent)

        self.SetBackgroundColour(wx.Colour(*SIDEBAR_BG_COLOR))
        self.SetMinSize(wx.Size(SIDEBAR_MIN_WIDTH_PX, -1))
        self.on_sidebar_toggle = on_toggle_callback

        self.sidebar_placeholder_label = wx.StaticText(
            self, label=SIDEBAR_PLACEHOLDER_TEXT, style=wx.ALIGN_CENTER
        )
        placeholder_font = self.sidebar_placeholder_label.GetFont()
        placeholder_font.PointSize = SIDEBAR_PLACEHOLDER_FONT_SIZE
        self.sidebar_placeholder_label.SetFont(placeholder_font)

        layout_sizer = wx.BoxSizer(wx.VERTICAL)
        layout_sizer.AddStretchSpacer()
        layout_sizer.Add(self.sidebar_placeholder_label, 0, wx.ALIGN_CENTER)
        layout_sizer.AddStretchSpacer()
        self.SetSizer(layout_sizer)

        # Start collapsed; the status bar's toggle button reveals it.
        self.Hide()

    def toggle_visibility(self) -> None:
        """Toggle whether the panel is shown and re-layout the parent frame."""
        self.Show(not self.IsShown())
        self.GetParent().Layout()
        
        # Call the toggle callback if provided
        if self.on_sidebar_toggle:
            self.on_sidebar_toggle(self.IsShown())
