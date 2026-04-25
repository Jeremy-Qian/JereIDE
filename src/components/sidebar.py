import wx

from constants import (
    SIDEBAR_BG_COLOR,
    SIDEBAR_MIN_WIDTH_PX,
    SIDEBAR_PLACEHOLDER_FONT_SIZE,
    SIDEBAR_PLACEHOLDER_TEXT,
)


class SideBar(wx.Panel):
    def __init__(self, parent, on_sidebar_toggle=None):
        """Initialize the sidebar as two stacked panels:
        - Top panel with two horizontally arranged action buttons
        - Bottom panel containing a placeholder label (unchanged)
        The top panel has a fixed height (driven by its content), and the bottom
        panel expands to fill the remaining space.
        """
        super().__init__(parent)

        self.SetBackgroundColour(wx.Colour(*SIDEBAR_BG_COLOR))
        self.SetMinSize(wx.Size(SIDEBAR_MIN_WIDTH_PX, -1))
        self.SetMaxSize(wx.Size(SIDEBAR_MIN_WIDTH_PX, -1))
        self.on_sidebar_toggle = on_sidebar_toggle

        # Top panel with two action buttons
        self.top_panel = wx.Panel(self)
        btn_build = wx.Button(self.top_panel, label="Project", style=wx.BORDER_NONE)
        btn_run = wx.Button(self.top_panel, label="Git", style=wx.BORDER_NONE)

        btn_build.Bind(wx.EVT_BUTTON, self._on_build)
        btn_run.Bind(wx.EVT_BUTTON, self._on_run)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(btn_build, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        top_sizer.Add(btn_run, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.top_panel.SetSizer(top_sizer)

        # Bottom panel with placeholder text (unchanged)
        self.bottom_panel = wx.Panel(self)
        bottom_label = wx.StaticText(self.bottom_panel, label=SIDEBAR_PLACEHOLDER_TEXT, style=wx.ALIGN_CENTER)
        font = bottom_label.GetFont()
        font.PointSize = SIDEBAR_PLACEHOLDER_FONT_SIZE
        bottom_label.SetFont(font)

        bottom_sizer = wx.BoxSizer(wx.VERTICAL)
        bottom_sizer.AddStretchSpacer()
        bottom_sizer.Add(bottom_label, 0, wx.ALIGN_CENTER)
        bottom_sizer.AddStretchSpacer()
        self.bottom_panel.SetSizer(bottom_sizer)

        # Separator between top and bottom panels
        self.separator_line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)

        # Layout: top panel, separator, bottom panel
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.top_panel, flag=wx.EXPAND)
        main_sizer.Add(self.separator_line, flag=wx.EXPAND)
        main_sizer.Add(self.bottom_panel, proportion=1, flag=wx.EXPAND)
        self.SetSizer(main_sizer)

        # Start collapsed; the status bar's toggle button reveals it.
        self.Hide()

    def toggle_visibility(self) -> None:
        """Toggle whether the panel is shown and re-layout the parent frame."""
        self.Show(not self.IsShown())
        self.GetParent().Layout()

        # Call the toggle callback if provided
        if self.on_sidebar_toggle:
            self.on_sidebar_toggle(self.IsShown())

    def _on_build(self, event: wx.CommandEvent) -> None:
        """Placeholder action for the Build button."""
        wx.MessageBox("Build not implemented yet.", "Sidebar", wx.OK | wx.ICON_INFORMATION, self)

    def _on_run(self, event: wx.CommandEvent) -> None:
        """Placeholder action for the Run button."""
        wx.MessageBox("Run not implemented yet.", "Sidebar", wx.OK | wx.ICON_INFORMATION, self)
