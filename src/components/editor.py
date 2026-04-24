import wx
import wx.stc

from constants import (
    EDITOR_CARET_PERIOD_MS,
    EDITOR_FONT_SIZE,
    INITIAL_LINE_NUMBER_MARGIN_WIDTH_PX,
    LINE_NUMBER_MARGIN_ID,
    LINE_NUMBER_MARGIN_PADDING_PX,
)
from utils.editor_helpers import (
    apply_caret_and_selection_styles,
    apply_indentation_settings,
    apply_lexer_settings,
    apply_python_syntax_styles,
    build_default_style_spec,
    configure_eol_and_whitespace,
    configure_fold_markers,
    configure_margins,
)


class Editor(wx.stc.StyledTextCtrl):
    def __init__(self, parent, file_path: str | None = None, style=wx.BORDER_NONE):
        super().__init__(parent, style=style)
        self.file_path = file_path
        self.line_numbers_enabled = True
        self._setup_editor()

    def set_value(self, value):
        was_read_only = self.GetReadOnly()
        self.SetReadOnly(False)
        self.SetText(value)
        self.EmptyUndoBuffer()
        self.SetSavePoint()
        self.SetReadOnly(was_read_only)

    def set_editable(self, is_editable):
        self.SetReadOnly(not is_editable)

    def is_modified(self):
        return self.GetModify()

    def clear_content(self):
        self.ClearAll()

    def set_insertion_point(self, position):
        self.SetCurrentPos(position)
        self.SetAnchor(position)

    def show_position(self, position):
        line_number = self.LineFromPosition(position)
        self.GotoLine(line_number)

    def get_last_position(self):
        return self.GetLength()

    def get_position_from_line(self, line_number):
        return self.PositionFromLine(line_number)

    def get_text_range(self, start_position, end_position):
        return self.GetTextRange(start_position, end_position)

    def get_selection_range(self):
        return self.GetAnchor(), self.GetCurrentPos()

    def set_selection_range(self, start_position, end_position):
        self.SetSelectionStart(start_position)
        self.SetSelectionEnd(end_position)

    def select_line(self, line_number):
        start_position = self.PositionFromLine(line_number)
        end_position = self.GetLineEndPosition(line_number)
        self.set_selection_range(start_position, end_position)

    def goto_line(self, line_number):
        position = self.get_position_from_line(line_number)
        self.set_insertion_point(position)
        self.show_position(position)

    def register_modified_event(self, event_handler):
        self.Bind(wx.stc.EVT_STC_CHANGE, event_handler)

    def _handle_margin_click(self, event):
        line = self.LineFromPosition(event.GetPosition())
        self.ToggleFold(line)
        event.Skip()

    def _setup_editor(self):
        default_style_spec = build_default_style_spec()
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, default_style_spec)
        self.StyleClearAll()
        self.SetUseHorizontalScrollBar(False)
        self.SetWrapMode(wx.stc.STC_WRAP_WORD)
        apply_lexer_settings(self)
        configure_margins(self)
        apply_indentation_settings(self)
        configure_eol_and_whitespace(self)
        configure_fold_markers(self)
        self.Bind(wx.stc.EVT_STC_MARGINCLICK, self._handle_margin_click)

        apply_python_syntax_styles(self)
        apply_caret_and_selection_styles(self)

        try:
            self.SetCaretPeriod(EDITOR_CARET_PERIOD_MS)
        except ValueError:
            pass

    def update_line_number_margin(self):
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

    def toggle_line_numbers(self):
        self.line_numbers_enabled = not self.line_numbers_enabled
        self.update_line_number_margin()
