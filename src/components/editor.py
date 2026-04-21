import wx
import wx.stc
from constants import (
    EDITOR_FONT_FACE,
    EDITOR_FONT_SIZE,
    LINE_NUMBER_MARGIN_ID,
    INITIAL_MARGIN_WIDTH,
    MARGIN_PADDING
)

class Editor(wx.stc.StyledTextCtrl):
    def __init__(self, parent):
        super(Editor, self).__init__(parent, style=wx.TE_MULTILINE)
        self.line_numbers_enabled = True
        self.init_ui()

    def init_ui(self):
        """Initialize the editor with fonts, margins, and wrapping."""
        font = wx.Font(
            EDITOR_FONT_SIZE,
            wx.FONTFAMILY_MODERN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            EDITOR_FONT_FACE,
        )

        self.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, font)
        self.StyleSetSize(wx.stc.STC_STYLE_DEFAULT, EDITOR_FONT_SIZE)
        self.StyleClearAll()

        self.SetMarginType(LINE_NUMBER_MARGIN_ID, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(LINE_NUMBER_MARGIN_ID, INITIAL_MARGIN_WIDTH)

        self.SetUseHorizontalScrollBar(False)
        self.SetWrapMode(wx.stc.STC_WRAP_WORD)
        
        self.update_line_number_margin()

    def update_line_number_margin(self):
        """Adjust the width of the line‑number margin so numbers never get clipped."""
        if not self.line_numbers_enabled:
            self.SetMarginWidth(LINE_NUMBER_MARGIN_ID, 0)
            return

        line_count = self.GetLineCount()
        digit_count = len(str(line_count))
        margin_width = self.TextWidth(
            wx.stc.STC_STYLE_LINENUMBER, "9" * digit_count
        ) + MARGIN_PADDING
        self.SetMarginWidth(LINE_NUMBER_MARGIN_ID, margin_width)

    def toggle_line_numbers(self):
        """Toggle the visibility of the line‑number margin."""
        self.line_numbers_enabled = not self.line_numbers_enabled
        self.update_line_number_margin()