"""Editor utility functions for styling, keywords, and configuration helpers."""

import keyword

import wx.stc

from constants import (
    EDITOR_BG_COLOR_BRACEBAD,
    EDITOR_BG_COLOR_BRACELIGHT,
    EDITOR_BG_COLOR_COMMENT,
    EDITOR_BG_COLOR_DEFAULT,
    EDITOR_BG_COLOR_LINENUMBER,
    EDITOR_BG_COLOR_TRIPLE,
    EDITOR_FG_COLOR_BRACEBAD,
    EDITOR_FG_COLOR_BRACELIGHT,
    EDITOR_FG_COLOR_CLASSNAME,
    EDITOR_FG_COLOR_COMMENT,
    EDITOR_FG_COLOR_DEFAULT,
    EDITOR_FG_COLOR_DEFNAM,
    EDITOR_FG_COLOR_INDENTGUIDE,
    EDITOR_FG_COLOR_KEYWORD,
    EDITOR_FG_COLOR_LINENUMBER,
    EDITOR_FG_COLOR_NUMBER,
    EDITOR_FG_COLOR_OPERATOR,
    EDITOR_FG_COLOR_STRING,
    EDITOR_FONT_FACE_MAC,
    EDITOR_FG_COLOR_IDENTIFIER,
)


def get_editor_font_face():
    """Get the appropriate font face for the current platform."""
    from constants import EDITOR_FONT_FACE_MAC
    return EDITOR_FONT_FACE_MAC


def get_editor_font_size():
    """Get the default font size for the editor."""
    from constants import EDITOR_FONT_SIZE
    return EDITOR_FONT_SIZE


def build_default_style_spec():
    """Build the default style specification for the editor."""
    font_face = get_editor_font_face()
    font_size = get_editor_font_size()
    return f'fore:{EDITOR_FG_COLOR_DEFAULT},back:{EDITOR_BG_COLOR_DEFAULT},face:{font_face},size:{font_size}'


def build_style_foreground_only(fg_color):
    """Build a style spec with only foreground color."""
    return f'fore:{fg_color}'


def build_style_fg_bg(fg_color, bg_color):
    """Build a style spec with foreground and background colors."""
    return f'fore:{fg_color},back:{bg_color}'


def build_style_bold(fg_color):
    """Build a style spec with bold attribute."""
    return f'fore:{fg_color},bold'


def build_style_fg_bg_bold(fg_color, bg_color):
    """Build a style spec with foreground, background, and bold."""
    return f'fore:{fg_color},back:{bg_color},bold'


def get_python_keywords_string():
    """Get Python keywords as a space-separated string for STC."""
    return " ".join(keyword.kwlist)


def configure_fold_markers(stc_control):
    """Configure fold markers for the editor."""
    stc_control.MarkerDefine(
        wx.stc.STC_MARKNUM_FOLDEREND,
        wx.stc.STC_MARK_BOXPLUSCONNECTED,
        "white",
        "black"
    )
    stc_control.MarkerDefine(
        wx.stc.STC_MARKNUM_FOLDEROPENMID,
        wx.stc.STC_MARK_BOXMINUSCONNECTED,
        "white",
        "black"
    )
    stc_control.MarkerDefine(
        wx.stc.STC_MARKNUM_FOLDERMIDTAIL,
        wx.stc.STC_MARK_TCORNER,
        "white",
        "black"
    )
    stc_control.MarkerDefine(
        wx.stc.STC_MARKNUM_FOLDERTAIL,
        wx.stc.STC_MARK_LCORNER,
        "white",
        "black"
    )
    stc_control.MarkerDefine(
        wx.stc.STC_MARKNUM_FOLDERSUB,
        wx.stc.STC_MARK_VLINE,
        "white",
        "black"
    )
    stc_control.MarkerDefine(
        wx.stc.STC_MARKNUM_FOLDER,
        wx.stc.STC_MARK_BOXPLUS,
        "white",
        "black"
    )
    stc_control.MarkerDefine(
        wx.stc.STC_MARKNUM_FOLDEROPEN,
        wx.stc.STC_MARK_BOXMINUS,
        "white",
        "black"
    )


def apply_python_syntax_styles(stc_control):
    """Apply Python syntax highlighting styles to the editor."""
    stc_control.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, build_style_fg_bg(
        EDITOR_FG_COLOR_LINENUMBER,
        EDITOR_BG_COLOR_LINENUMBER
    ))
    stc_control.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, build_style_fg_bg(
        EDITOR_FG_COLOR_BRACELIGHT,
        EDITOR_BG_COLOR_BRACELIGHT
    ))
    stc_control.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, build_style_fg_bg(
        EDITOR_FG_COLOR_BRACEBAD,
        EDITOR_BG_COLOR_BRACEBAD
    ))
    stc_control.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, build_style_foreground_only(
        EDITOR_FG_COLOR_INDENTGUIDE
    ))

    stc_control.StyleSetSpec(wx.stc.STC_P_DEFAULT, build_style_foreground_only(
        EDITOR_FG_COLOR_DEFAULT
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, build_style_fg_bg(
        EDITOR_FG_COLOR_COMMENT,
        EDITOR_BG_COLOR_COMMENT
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, build_style_fg_bg(
        EDITOR_FG_COLOR_COMMENT,
        EDITOR_BG_COLOR_COMMENT
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_NUMBER, build_style_foreground_only(
        EDITOR_FG_COLOR_NUMBER
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_STRING, build_style_foreground_only(
        EDITOR_FG_COLOR_STRING
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_CHARACTER, build_style_foreground_only(
        EDITOR_FG_COLOR_STRING
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_WORD, build_style_bold(
        EDITOR_FG_COLOR_KEYWORD
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_TRIPLE, build_style_fg_bg(
        EDITOR_FG_COLOR_STRING,
        EDITOR_BG_COLOR_TRIPLE
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, build_style_fg_bg(
        EDITOR_FG_COLOR_STRING,
        EDITOR_BG_COLOR_TRIPLE
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_CLASSNAME, build_style_bold(
        EDITOR_FG_COLOR_CLASSNAME
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_DEFNAME, build_style_bold(
        EDITOR_FG_COLOR_DEFNAM
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_OPERATOR, build_style_bold(
        EDITOR_FG_COLOR_OPERATOR
    ))
    stc_control.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, build_style_foreground_only(
        EDITOR_FG_COLOR_IDENTIFIER
    ))


def apply_caret_and_selection_styles(stc_control):
    """Apply caret and selection styles to the editor."""
    from constants import EDITOR_CARET_COLOR, EDITOR_SELECTION_COLOR

    stc_control.SetCaretForeground(EDITOR_CARET_COLOR)
    stc_control.SetSelBackground(1, EDITOR_SELECTION_COLOR)

    stc_control.SetSelBackground(
        True,
        wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
    )
    stc_control.SetSelForeground(
        True,
        wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
    )


def apply_indentation_settings(stc_control):
    """Apply indentation settings to the editor."""
    from constants import (
        EDITOR_INDENT_SIZE,
        EDITOR_TAB_WIDTH,
        EDITOR_USE_TABS,
    )

    stc_control.SetIndent(EDITOR_INDENT_SIZE)
    stc_control.SetIndentationGuides(True)
    stc_control.SetBackSpaceUnIndents(True)
    stc_control.SetTabIndents(True)
    stc_control.SetTabWidth(EDITOR_TAB_WIDTH)
    stc_control.SetUseTabs(EDITOR_USE_TABS)


def configure_margins(stc_control):
    """Configure editor margins (line numbers and fold)."""
    from constants import (
        EDITOR_MARGIN_LEFT_PX,
        EDITOR_MARGIN_RIGHT_PX,
        EDITOR_FOLD_MARGIN_ID,
        EDITOR_FOLD_MARGIN_WIDTH_PX,
        INITIAL_LINE_NUMBER_MARGIN_WIDTH_PX,
        LINE_NUMBER_MARGIN_ID,
    )

    stc_control.SetMargins(EDITOR_MARGIN_LEFT_PX, EDITOR_MARGIN_RIGHT_PX)

    stc_control.SetMarginType(LINE_NUMBER_MARGIN_ID, wx.stc.STC_MARGIN_NUMBER)
    stc_control.SetMarginWidth(LINE_NUMBER_MARGIN_ID, INITIAL_LINE_NUMBER_MARGIN_WIDTH_PX)
    stc_control.SetMarginCursor(LINE_NUMBER_MARGIN_ID, -1)

    stc_control.SetMarginType(EDITOR_FOLD_MARGIN_ID, wx.stc.STC_MARGIN_SYMBOL)
    stc_control.SetMarginMask(EDITOR_FOLD_MARGIN_ID, wx.stc.STC_MASK_FOLDERS)
    stc_control.SetMarginSensitive(EDITOR_FOLD_MARGIN_ID, True)
    stc_control.SetMarginWidth(EDITOR_FOLD_MARGIN_ID, EDITOR_FOLD_MARGIN_WIDTH_PX)
    stc_control.SetMarginCursor(EDITOR_FOLD_MARGIN_ID, -1)


def apply_lexer_settings(stc_control):
    """Apply lexer settings to the editor."""
    from constants import EDITOR_FOLD_ENABLED, EDITOR_TAB_WHINGE_LEVEL

    stc_control.SetLexer(wx.stc.STC_LEX_PYTHON)
    stc_control.SetKeyWords(0, get_python_keywords_string())

    stc_control.SetProperty("fold", "1" if EDITOR_FOLD_ENABLED else "0")
    stc_control.SetProperty("tab.timmy.whinge.level", EDITOR_TAB_WHINGE_LEVEL)


def configure_eol_and_whitespace(stc_control):
    """Configure EOL mode and whitespace visibility."""
    stc_control.SetEOLMode(wx.stc.STC_EOL_LF)
    stc_control.SetViewEOL(False)
    stc_control.SetViewWhiteSpace(False)
    stc_control.SetEdgeMode(wx.stc.STC_EDGE_NONE)