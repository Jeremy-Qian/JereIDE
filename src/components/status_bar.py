import wx
import wx.lib.platebtn as platebtn

from constants import (
    INITIAL_CURSOR_POSITION_LABEL,
    SIDEBAR_TOGGLE_ICON_HEIGHT_PX,
    SIDEBAR_TOGGLE_ICON_FILENAME,
    SIDEBAR_TOGGLE_ICON_WIDTH_PX,
    STATUS_BAR_BUTTON_PRESS_COLOR,
    STATUS_BAR_BG_COLOR,
    STATUS_BAR_HEIGHT_PX,
)
from utils.paths import icon_path


def _load_sidebar_toggle_icon(icon_filename: str) -> wx.Bitmap:
    """Load and rescale a sidebar-toggle icon to the configured dimensions."""
    icon_image = wx.Image(icon_path(icon_filename))
    icon_image.Rescale(SIDEBAR_TOGGLE_ICON_WIDTH_PX, SIDEBAR_TOGGLE_ICON_HEIGHT_PX)
    return wx.Bitmap(icon_image)


class StatusBar(wx.Panel):
    def __init__(self, parent):
        """Initialize the status bar with a fixed height and line/column display."""
        super().__init__(parent)

        self.SetBackgroundColour(STATUS_BAR_BG_COLOR)

        # Fix the height so the panel behaves like a traditional status bar.
        self.SetMinSize((-1, STATUS_BAR_HEIGHT_PX))
        self.SetMaxSize((-1, STATUS_BAR_HEIGHT_PX))

        # Pre-load the sidebar-toggle icon so clicks are cheap.
        self.sidebar_toggle_icon = _load_sidebar_toggle_icon(SIDEBAR_TOGGLE_ICON_FILENAME)

        self.sidebar_toggle_btn = platebtn.PlateButton(
            self, bmp=self.sidebar_toggle_icon
        )
        self.sidebar_toggle_btn.SetPressColor(wx.Colour(*STATUS_BAR_BUTTON_PRESS_COLOR))

        self.text_indicator = platebtn.PlateButton(self, label=INITIAL_CURSOR_POSITION_LABEL)
        self.text_indicator.SetPressColor(wx.Colour(*STATUS_BAR_BUTTON_PRESS_COLOR))

        layout_sizer = wx.BoxSizer(wx.HORIZONTAL)
        layout_sizer.Add(self.sidebar_toggle_btn, 0, wx.LEFT | wx.RIGHT, 2)
        layout_sizer.Add(self.text_indicator, 0, wx.LEFT, 0)
        self.SetSizer(layout_sizer)

        # Populated later via set_sidebar().
        self.sidebar: wx.Panel | None = None

    def update_status(self, line_number: int, column_number: int) -> None:
        """Update the panel text with the current line and column.

        Args:
            line_number: The current line number (1-indexed).
            column_number: The current column number (0-indexed).
        """
        self.text_indicator.SetLabel(f"{line_number}:{column_number}")
        # Force the button to resize to fit the new text.
        self.Layout()

    def update_from_editor(self, editor) -> None:
        """Extract line and column from a StyledTextCtrl and refresh the status.

        Args:
            editor: The ``wx.stc.StyledTextCtrl`` instance.
        """
        cursor_position = editor.GetCurrentPos()
        line_number = editor.LineFromPosition(cursor_position) + 1
        column_number = editor.GetColumn(cursor_position)
        self.update_status(line_number, column_number)

    def set_sidebar(self, sidebar: wx.Panel) -> None:
        """Set the sidebar reference for toggling.

        Args:
            sidebar: The ``SideBar`` instance to toggle.
        """
        self.sidebar = sidebar

    def on_toggle_sidebar(self, event: wx.CommandEvent | None) -> None:
        """Handle the sidebar toggle button click."""

        if self.sidebar is not None:
            self.sidebar.toggle_visibility()

        if event is not None:
            event.Skip()
