import wx

class StatusBar(wx.StatusBar):
    def __init__(self, parent):
        """Initialize the status bar with a single field for line and column info."""
        super(StatusBar, self).__init__(parent)
        self.SetFieldsCount(1)
        # Set a light gray background color as seen in the test script
        self.SetBackgroundColour((220, 220, 220))
        self.update_status(1, 0)

    def update_status(self, line, column):
        """
        Update the status bar text with the current line and column.
        
        Args:
            line: The current line number (1-indexed).
            column: The current column number (0-indexed).
        """
        status_text = f"Line {line}, Column {column}"
        self.SetStatusText(status_text, 0)

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