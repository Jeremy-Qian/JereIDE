import wx
import wx.stc

from constants import (
    EDITOR_FONT_FACE,
    EDITOR_FONT_SIZE,
    INITIAL_LINE_NUMBER_MARGIN_WIDTH_PX,
    LINE_NUMBER_MARGIN_ID,
    LINE_NUMBER_MARGIN_PADDING_PX,
)


class Editor(wx.stc.StyledTextCtrl):
    def __init__(self, parent):
        super().__init__(parent, style=wx.TE_MULTILINE)
        self.line_numbers_enabled = True
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the editor with fonts, margins, and wrapping."""
        editor_font = wx.Font(
            EDITOR_FONT_SIZE,
            wx.FONTFAMILY_MODERN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            EDITOR_FONT_FACE,
        )

        self.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, editor_font)
        self.StyleSetSize(wx.stc.STC_STYLE_DEFAULT, EDITOR_FONT_SIZE)
        self.StyleClearAll()

        self.SetMarginType(LINE_NUMBER_MARGIN_ID, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(LINE_NUMBER_MARGIN_ID, INITIAL_LINE_NUMBER_MARGIN_WIDTH_PX)

        self.SetUseHorizontalScrollBar(False)
        self.SetWrapMode(wx.stc.STC_WRAP_WORD)

        self.update_line_number_margin()

    def update_line_number_margin(self) -> None:
        """Adjust the width of the line‑number margin so numbers never get clipped."""
        if not self.line_numbers_enabled:
            self.SetMarginWidth(LINE_NUMBER_MARGIN_ID, 0)
            return

        line_count = self.GetLineCount()
        digit_count = len(str(line_count))
        margin_width_px = (
            self.TextWidth(wx.stc.STC_STYLE_LINENUMBER, "9" * digit_count)
            + LINE_NUMBER_MARGIN_PADDING_PX
        )
        self.SetMarginWidth(LINE_NUMBER_MARGIN_ID, margin_width_px)

    def toggle_line_numbers(self) -> None:
        """Toggle the visibility of the line‑number margin."""
        self.line_numbers_enabled = not self.line_numbers_enabled
        self.update_line_number_margin()
