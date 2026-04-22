import wx
import wx.lib.platebtn as pbtn
import os

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

        # Create the toggle project panel button
        # Load the custom icon for the toggle project button
        self.toggle_off = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "icons", "archivebox.png")
        self.toggle_off = wx.Image(self.toggle_off)
        self.toggle_off.Rescale(18, 16)
        self.icon_off = wx.Bitmap(self.toggle_off)
        self.toggle_on = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "icons", "archivebox.fill.png")
        self.toggle_on = wx.Image(self.toggle_on)
        self.toggle_on.Rescale(18, 16)
        self.icon_on = wx.Bitmap(self.toggle_on)
        self.toggle_project_btn = pbtn.PlateButton(self, bmp=self.icon_off)
        self.toggle_project_btn.SetPressColor(wx.Colour(200, 200, 200))

        self.status_text = pbtn.PlateButton(self, label="1:0")
        self.status_text.SetPressColor(wx.Colour(200, 200, 200))

        # Layout the elements with padding
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.toggle_project_btn, 0, wx.LEFT | wx.RIGHT, 2)
        sizer.Add(self.status_text, 0, wx.LEFT, 0)
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
        # Force the button to resize to fit the new text
        self.Layout()

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

    def set_project_panel(self, project_panel):
        """
        Set the project panel reference for toggling.

        Args:
            project_panel: The ProjectPanel instance to toggle.
        """
        self.project_panel = project_panel

    def on_toggle_project_panel(self, event):
        """
        Handle the toggle project panel button click.
        """
        if self.toggle_project_btn.GetBitmapLabel() == self.icon_off:
            self.toggle_project_btn.SetBitmap(self.icon_on)
        else:
            self.toggle_project_btn.SetBitmap(self.icon_off)
        if hasattr(self, 'project_panel'):
            self.project_panel.toggle_project_panel()
        if event:
            event.Skip()
