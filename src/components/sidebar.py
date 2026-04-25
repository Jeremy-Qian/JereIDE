import os
import wx

from constants import (
    BUTTON_ICON_HEIGHT_PX,
    BUTTON_ICON_WIDTH_PX,
    GIT_ICON_FILENAME,
    ICONS_DIR_NAME,
    PROJECT_ICON_FILENAME,
    SEARCH_ICON_FILENAME,
    SIDEBAR_BG_COLOR,
    SIDEBAR_MIN_WIDTH_PX,
    SIDEBAR_PLACEHOLDER_FONT_SIZE,
    SIDEBAR_PLACEHOLDER_TEXT,
)
from components.find_replace_dialog import show_find_dialog


def _load_button_icon(icon_filename: str) -> wx.Bitmap:
    """Load and rescale a button icon to the configured dimensions."""
    icon_path = os.path.join(ICONS_DIR_NAME, icon_filename)
    icon_image = wx.Image(icon_path)
    icon_image.Rescale(BUTTON_ICON_WIDTH_PX, BUTTON_ICON_HEIGHT_PX, quality=wx.IMAGE_QUALITY_BICUBIC)
    return wx.Bitmap(icon_image)


class SideBar(wx.Panel):
    def __init__(self, main_frame, on_sidebar_toggle=None):
        """Initialize the sidebar as two stacked panels:
        - Top panel with two horizontally arranged action buttons
        - Bottom panel containing a placeholder label (unchanged)
        The top panel has a fixed height (driven by its content), and the bottom
        panel expands to fill the remaining space.
        """
        super().__init__(main_frame)

        self.main_frame = main_frame
        self.SetBackgroundColour(wx.Colour(*SIDEBAR_BG_COLOR))
        self.SetMinSize(wx.Size(SIDEBAR_MIN_WIDTH_PX, -1))
        self.SetMaxSize(wx.Size(SIDEBAR_MIN_WIDTH_PX, -1))
        self.on_sidebar_toggle = on_sidebar_toggle

        # Top panel with two action buttons
        self.top_panel = wx.Panel(self)
        btn_project = wx.BitmapButton(self.top_panel, style=wx.BORDER_NONE)
        btn_git = wx.BitmapButton(self.top_panel, style=wx.BORDER_NONE)
        btn_search = wx.BitmapButton(self.top_panel, style=wx.BORDER_NONE)

        # Load and set icons for buttons
        project_icon = _load_button_icon(PROJECT_ICON_FILENAME)
        git_icon = _load_button_icon(GIT_ICON_FILENAME)
        search_icon = _load_button_icon(SEARCH_ICON_FILENAME)
        btn_project.SetBitmap(project_icon)
        btn_git.SetBitmap(git_icon)
        btn_search.SetBitmap(search_icon)

        btn_project.Bind(wx.EVT_BUTTON, self._on_project)
        btn_git.Bind(wx.EVT_BUTTON, self._on_git)
        btn_search.Bind(wx.EVT_BUTTON, self._on_search)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.AddStretchSpacer()
        top_sizer.Add(btn_project, 0, wx.ALL, border=5)
        top_sizer.Add(btn_git, 0, wx.ALL, border=5)
        top_sizer.Add(btn_search, 0, wx.ALL, border=5)
        top_sizer.AddStretchSpacer()
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

    def _on_project(self, event: wx.CommandEvent) -> None:
        """Placeholder action for the Project button."""
        pass

    def _on_search(self, event: wx.CommandEvent) -> None:
        """Handle the Search button click."""
        editor = self.main_frame.get_current_editor()
        if editor:
            show_find_dialog(self.main_frame, editor)

    def _on_git(self, event: wx.CommandEvent) -> None:
        """Placeholder action for the Git button."""
        pass
