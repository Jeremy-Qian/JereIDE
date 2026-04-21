import wx
import wx.lib.platebtn as pbtn
class StatusPanel(wx.Panel):
    def __init__(self, parent):
        """Initialize the status panel with a fixed height and line/column display."""
        super(StatusPanel, self).__init__(parent)

        # Set a light gray background color
        self.SetBackgroundColour((220, 220, 220))

        # Fix the height to make it behave like a traditional status bar (non-resizable vertically)
        self.SetMinSize((-1, 25))
        self.SetMaxSize((-1, 25))

        # Create the text label for status
        self.status_text = pbtn.PlateButton(self, label="1:0")
        self.status_text.SetPressColor(wx.Colour(200, 200, 200))
        # Layout the text with some padding
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.status_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        self.SetSizer(sizer)

    def update_status(self, line, column):
        """
        Update the panel text with the current line and column.

        Args:
            line: The current line number (1-indexed).
            column: The current column number (0-indexed).
        """
        status_text = f"{line}:{column}"
        self.status_text.SetLabel(status_text)

    def update_from_editor(self, editor):
        """
        Extract line and column information from a StyledTextCtrl and update the status.

        Args:
            editor: The wx.stc.StyledTextCtrl instance.
        """
        current_pos = editor.GetCurrentPos()
        line = editor.LineFromPosition(current_pos) + 1
        column = editor.GetColumn(current_pos)
        self.update_status(line, column)
