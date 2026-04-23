import wx
import wx.stc
import keyword

from constants import (
    EDITOR_FONT_FACE,
    EDITOR_FONT_SIZE,
    INITIAL_LINE_NUMBER_MARGIN_WIDTH_PX,
    LINE_NUMBER_MARGIN_ID,
    LINE_NUMBER_MARGIN_PADDING_PX,
)


class Editor(wx.stc.StyledTextCtrl):
    def __init__(self, parent, style=wx.BORDER_NONE):
        super().__init__(parent, style=style)
        self.line_numbers_enabled = True
        self.SetUpEditor()

    def SetValue(self, value):
        val = self.GetReadOnly()
        self.SetReadOnly(False)
        self.SetText(value)
        self.EmptyUndoBuffer()
        self.SetSavePoint()
        self.SetReadOnly(val)

    def SetEditable(self, val):
        self.SetReadOnly(not val)

    def IsModified(self):
        return self.GetModify()

    def Clear(self):
        self.ClearAll()

    def SetInsertionPoint(self, pos):
        self.SetCurrentPos(pos)
        self.SetAnchor(pos)

    def ShowPosition(self, pos):
        line = self.LineFromPosition(pos)
        self.GotoLine(line)

    def GetLastPosition(self):
        return self.GetLength()

    def GetPositionFromLine(self, line):
        return self.PositionFromLine(line)

    def GetRange(self, start, end):
        return self.GetTextRange(start, end)

    def GetSelection(self):
        return self.GetAnchor(), self.GetCurrentPos()

    def SetSelection(self, start, end):
        self.SetSelectionStart(start)
        self.SetSelectionEnd(end)

    def SelectLine(self, line):
        start = self.PositionFromLine(line)
        end = self.GetLineEndPosition(line)
        self.SetSelection(start, end)

    def GotoLine(self, line):
        pos = self.GetPositionFromLine(line)
        self.SetInsertionPoint(pos)
        self.ShowPosition(pos)

    def RegisterModifiedEvent(self, eventHandler):
        self.Bind(wx.stc.EVT_STC_CHANGE, eventHandler)

    def SetUpEditor(self):
        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")

        self.SetMargins(2, 2)

        self.SetMarginType(LINE_NUMBER_MARGIN_ID, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(LINE_NUMBER_MARGIN_ID, INITIAL_LINE_NUMBER_MARGIN_WIDTH_PX)

        self.SetIndent(4)
        self.SetIndentationGuides(True)
        self.SetBackSpaceUnIndents(True)
        self.SetTabIndents(True)
        self.SetTabWidth(4)
        self.SetUseTabs(False)

        self.SetViewWhiteSpace(False)

        self.SetEOLMode(wx.stc.STC_EOL_LF)
        self.SetViewEOL(False)

        self.SetEdgeMode(wx.stc.STC_EDGE_NONE)

        self.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUSCONNECTED, "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER, "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_LCORNER, "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_VLINE, "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS, "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS, "white", "black")

        if wx.Platform == '__WXMSW__':
            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Courier New')
        elif wx.Platform == '__WXMAC__':
            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Monaco')
        else:
            defsize = wx.SystemSettings.GetFont(wx.SYS_ANSI_FIXED_FONT).GetPointSize()
            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Courier,size:%d' % defsize)

        self.StyleClearAll()

        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, 'fore:#000000,back:#99A9C2')
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, 'fore:#00009D,back:#FFFF00')
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, 'fore:#00009D,back:#FF0000')
        self.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")

        self.StyleSetSpec(wx.stc.STC_P_DEFAULT, 'fore:#000000')
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, 'fore:#008000,back:#F0FFF0')
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, 'fore:#008000,back:#F0FFF0')
        self.StyleSetSpec(wx.stc.STC_P_NUMBER, 'fore:#008080')
        self.StyleSetSpec(wx.stc.STC_P_STRING, 'fore:#800080')
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER, 'fore:#800080')
        self.StyleSetSpec(wx.stc.STC_P_WORD, 'fore:#000080,bold')
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE, 'fore:#800080,back:#FFFFEA')
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, 'fore:#800080,back:#FFFFEA')
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, 'fore:#0000FF,bold')
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME, 'fore:#008080,bold')
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR, 'fore:#800000,bold')
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, 'fore:#000000')

        self.SetCaretForeground("BLUE")
        self.SetSelBackground(1, '#66CCFF')

        try:
            self.SetCaretPeriod(530)
        except ValueError:
            pass

        self.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

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