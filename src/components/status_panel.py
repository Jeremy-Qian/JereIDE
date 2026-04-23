import wx
import wx.lib.platebtn as platebtn

from constants import (
    INITIAL_STATUS_LABEL,
    PROJECT_TOGGLE_ICON_HEIGHT_PX,
    PROJECT_TOGGLE_ICON_OFF_FILENAME,
    PROJECT_TOGGLE_ICON_ON_FILENAME,
    PROJECT_TOGGLE_ICON_WIDTH_PX,
    STATUS_BUTTON_PRESS_COLOR,
    STATUS_PANEL_BG_COLOR,
    STATUS_PANEL_HEIGHT_PX,
)
from utils.paths import icon_path


def _load_toggle_icon(icon_filename: str) -> wx.Bitmap:
    """Load and rescale a project-toggle icon to the configured dimensions."""
    icon_image = wx.Image(icon_path(icon_filename))
    icon_image.Rescale(PROJECT_TOGGLE_ICON_WIDTH_PX, PROJECT_TOGGLE_ICON_HEIGHT_PX)
    return wx.Bitmap(icon_image)


class StatusPanel(wx.Panel):
    def __init__(self, parent):
        """Initialize the status panel with a fixed height and line/column display."""
        super().__init__(parent)

        self.SetBackgroundColour(STATUS_PANEL_BG_COLOR)

        # Fix the height so the panel behaves like a traditional status bar.
        self.SetMinSize((-1, STATUS_PANEL_HEIGHT_PX))
        self.SetMaxSize((-1, STATUS_PANEL_HEIGHT_PX))

        # Pre-load both states of the project-toggle icon so clicks are cheap.
        self.project_toggle_icon_off = _load_toggle_icon(PROJECT_TOGGLE_ICON_OFF_FILENAME)
        self.project_toggle_icon_on = _load_toggle_icon(PROJECT_TOGGLE_ICON_ON_FILENAME)

        self.toggle_project_btn = platebtn.PlateButton(
            self, bmp=self.project_toggle_icon_off
        )
        self.toggle_project_btn.SetPressColor(wx.Colour(*STATUS_BUTTON_PRESS_COLOR))

        self.status_text = platebtn.PlateButton(self, label=INITIAL_STATUS_LABEL)
        self.status_text.SetPressColor(wx.Colour(*STATUS_BUTTON_PRESS_COLOR))

        layout_sizer = wx.BoxSizer(wx.HORIZONTAL)
        layout_sizer.Add(self.toggle_project_btn, 0, wx.LEFT | wx.RIGHT, 2)
        layout_sizer.Add(self.status_text, 0, wx.LEFT, 0)
        self.SetSizer(layout_sizer)

        # Populated later via set_sidebar().
        self.sidebar: wx.Panel | None = None

    def update_status(self, line_number: int, column_number: int) -> None:
        """Update the panel text with the current line and column.

        Args:
            line_number: The current line number (1-indexed).
            column_number: The current column number (0-indexed).
        """
        self.status_text.SetLabel(f"{line_number}:{column_number}")
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
        """Set the project panel reference for toggling.

        Args:
            sidebar: The ``SideBar`` instance to toggle.
        """
        self.sidebar = sidebar

    def on_toggle_sidebar(self, event: wx.CommandEvent | None) -> None:
        """Handle the toggle-project-panel button click."""
        is_currently_off = (
            self.toggle_project_btn.GetBitmapLabel() == self.project_toggle_icon_off
        )
        next_icon = (
            self.project_toggle_icon_on if is_currently_off else self.project_toggle_icon_off
        )
        self.toggle_project_btn.SetBitmap(next_icon)

        if self.sidebar is not None:
            self.sidebar.toggle_visibility()

        if event is not None:
            event.Skip()
