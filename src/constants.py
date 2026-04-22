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
OTHER_EDITED_SUFFIX = " •"

# ---------------------------------------------------------------------------
# Editor
# ---------------------------------------------------------------------------
EDITOR_FONT_FACE = "Menlo"
EDITOR_FONT_SIZE = 10
LINE_NUMBER_MARGIN_ID = 1
INITIAL_LINE_NUMBER_MARGIN_WIDTH_PX = 40
LINE_NUMBER_MARGIN_PADDING_PX = 4

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
MENU_OPEN_LABEL = "&Open...\tCtrl+O"
MENU_SAVE_LABEL = "&Save\tCtrl+S"

MENU_VIEW_LABEL = "&View"
MENU_TOGGLE_LINE_NUMBERS_LABEL = "Toggle &Line Numbers"

MENU_HELP_LABEL = "&Help"
MENU_ABOUT_LABEL = f"&About {APP_NAME}"

# ---------------------------------------------------------------------------
# Project panel
# ---------------------------------------------------------------------------
PROJECT_PANEL_BG_COLOR = (240, 240, 240)
PROJECT_PANEL_MIN_WIDTH_PX = 200
PROJECT_PANEL_PLACEHOLDER_TEXT = "Needs Implementation"
PROJECT_PANEL_PLACEHOLDER_FONT_SIZE = 12

# ---------------------------------------------------------------------------
# Status panel
# ---------------------------------------------------------------------------
STATUS_PANEL_BG_COLOR = (220, 220, 220)
STATUS_PANEL_HEIGHT_PX = 25
STATUS_BUTTON_PRESS_COLOR = (200, 200, 200)
INITIAL_STATUS_LABEL = "1:0"

# ---------------------------------------------------------------------------
# Icons
# ---------------------------------------------------------------------------
ICONS_DIR_NAME = "icons"
PROJECT_TOGGLE_ICON_OFF_FILENAME = "archivebox.png"
PROJECT_TOGGLE_ICON_ON_FILENAME = "archivebox.fill.png"
PROJECT_TOGGLE_ICON_WIDTH_PX = 18
PROJECT_TOGGLE_ICON_HEIGHT_PX = 16
