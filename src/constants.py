"""Application-wide constants for JereIDE.

Grouped by domain so new UI surfaces can pick the right constants without
grepping the codebase. Prefer adding a new constant here over hard-coding
a value in a component.
"""

# ---------------------------------------------------------------------------
# Application metadata
# ---------------------------------------------------------------------------
APP_NAME = "JereIDE"
APP_VERSION = "Beta"
APP_DESCRIPTION = (
    "JereIDE – a minimal IDE built with wxPython.\n"
    "Features include opening, saving, and basic text editing."
)
APP_COPYRIGHT = "Copyright (C) 2026 Jeremy-Qian"

# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------
DEFAULT_WINDOW_SIZE = (800, 600)
UNTITLED_NAME = "Untitled"
MACOS_EDITED_SUFFIX = " — Edited"

# ---------------------------------------------------------------------------
# Editor - Core
# ---------------------------------------------------------------------------
EDITOR_FONT_SIZE = 10
LINE_NUMBER_MARGIN_ID = 1
INITIAL_LINE_NUMBER_MARGIN_WIDTH_PX = 11
LINE_NUMBER_MARGIN_PADDING_PX = 4

# ---------------------------------------------------------------------------
# Editor - Indentation
# ---------------------------------------------------------------------------
EDITOR_INDENT_SIZE = 4
EDITOR_TAB_WIDTH = 4
EDITOR_USE_TABS = False

# ---------------------------------------------------------------------------
# Editor - Margins
# ---------------------------------------------------------------------------
EDITOR_MARGIN_LEFT_PX = 2
EDITOR_MARGIN_RIGHT_PX = 2
EDITOR_FOLD_MARGIN_ID = 2
EDITOR_FOLD_MARGIN_WIDTH_PX = 12

# ---------------------------------------------------------------------------
# Editor - Colors (STC Style Specs)
# ---------------------------------------------------------------------------
EDITOR_FG_COLOR_DEFAULT = "#000000"
EDITOR_BG_COLOR_DEFAULT = "#FFFFFF"
EDITOR_FG_COLOR_COMMENT = "#008000"
EDITOR_BG_COLOR_COMMENT = "#F0FFF0"
EDITOR_FG_COLOR_NUMBER = "#008080"
EDITOR_FG_COLOR_STRING = "#800080"
EDITOR_FG_COLOR_KEYWORD = "#000080"
EDITOR_BG_COLOR_TRIPLE = "#FFFFEA"
EDITOR_FG_COLOR_CLASSNAME = "#0000FF"
EDITOR_FG_COLOR_DEFNAM = "#008080"
EDITOR_FG_COLOR_OPERATOR = "#800000"
EDITOR_FG_COLOR_IDENTIFIER = "#000000"
EDITOR_FG_COLOR_LINENUMBER = "#000000"
EDITOR_BG_COLOR_LINENUMBER = "#99A9C2"
EDITOR_FG_COLOR_BRACELIGHT = "#00009D"
EDITOR_BG_COLOR_BRACELIGHT = "#FFFF00"
EDITOR_FG_COLOR_BRACEBAD = "#00009D"
EDITOR_BG_COLOR_BRACEBAD = "#FF0000"
EDITOR_FG_COLOR_INDENTGUIDE = "#CDCDCD"
EDITOR_CARET_COLOR = "BLUE"
EDITOR_SELECTION_COLOR = "#66CCFF"
EDITOR_HIGHLIGHT_BG = None  # Uses system default
EDITOR_HIGHLIGHT_FG = None  # Uses system default

# ---------------------------------------------------------------------------
# Editor - Fonts (Platform-specific)
# ---------------------------------------------------------------------------
EDITOR_FONT_FACE_MAC = "Monaco"

# ---------------------------------------------------------------------------
# Editor - Caret
# ---------------------------------------------------------------------------
EDITOR_CARET_PERIOD_MS = 530

# ---------------------------------------------------------------------------
# Editor - Lexer Properties
# ---------------------------------------------------------------------------
EDITOR_FOLD_ENABLED = True
EDITOR_TAB_WHINGE_LEVEL = "1"

# ---------------------------------------------------------------------------
# File dialog
# ---------------------------------------------------------------------------
FILE_WILDCARDS = "Text files (*.txt)|*.txt|All files (*.*)|*.*"
OPEN_DIALOG_TITLE = "Open file"
SAVE_DIALOG_TITLE = "Save file as"

# ---------------------------------------------------------------------------
# Menu labels
# ---------------------------------------------------------------------------
MENU_FILE_LABEL = "&File"
MENU_NEW_LABEL = "&New\tCtrl+N"
MENU_OPEN_LABEL = "&Open...\tCtrl+O"
MENU_SAVE_LABEL = "&Save\tCtrl+S"
MENU_SAVE_AS_LABEL = "Save &As...\tCtrl+Shift+S"
MENU_CLOSE_TAB_LABEL = "&Close Tab\tCtrl+W"

MENU_EDIT_LABEL = "&Edit"
MENU_FIND_LABEL = "&Find...\tCtrl+F"
MENU_FIND_NEXT_LABEL = "Find &Next\tF3"
MENU_REPLACE_LABEL = "&Replace...\tCtrl+H"

MENU_VIEW_LABEL = "&View"
MENU_TOGGLE_LINE_NUMBERS_LABEL = "Toggle &Line Numbers"

MENU_HELP_LABEL = "&Help"
MENU_ABOUT_LABEL = f"&About {APP_NAME}"

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
SIDEBAR_BG_COLOR = (240, 240, 240)
SIDEBAR_MIN_WIDTH_PX = 200
SIDEBAR_PLACEHOLDER_TEXT = "Needs Implementation"
SIDEBAR_PLACEHOLDER_FONT_SIZE = 12

# ---------------------------------------------------------------------------
# Status bar
# ---------------------------------------------------------------------------
STATUS_BAR_BG_COLOR = (220, 220, 220)
STATUS_BAR_HEIGHT_PX = 25
STATUS_BAR_BUTTON_PRESS_COLOR = (200, 200, 200)
INITIAL_CURSOR_POSITION_LABEL = "1:0"

# ---------------------------------------------------------------------------
# Icons
# ---------------------------------------------------------------------------
ICONS_DIR_NAME = "src/components/icons"
SIDEBAR_TOGGLE_ICON_FILENAME = "sidebar.left.png"
SIDEBAR_TOGGLE_ICON_WIDTH_PX = 20
SIDEBAR_TOGGLE_ICON_HEIGHT_PX = 16
PROJECT_ICON_FILENAME = "doc.on.doc.png"
GIT_ICON_FILENAME = "circle.grid.hex.png"
BUTTON_ICON_WIDTH_PX = 16
BUTTON_ICON_HEIGHT_PX = 16
