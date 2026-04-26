"""Menu bar creation for JereIDE."""

from PySide6.QtWidgets import QMenuBar, QMenu

from constants import (
    MENU_ABOUT_LABEL,
    MENU_CLOSE_TAB_LABEL,
    MENU_EDIT_LABEL,
    MENU_FILE_LABEL,
    MENU_FIND_LABEL,
    MENU_FIND_NEXT_LABEL,
    MENU_HELP_LABEL,
    MENU_NEW_LABEL,
    MENU_OPEN_LABEL,
    MENU_REPLACE_LABEL,
    MENU_SAVE_AS_LABEL,
    MENU_SAVE_LABEL,
    MENU_TOGGLE_LINE_NUMBERS_LABEL,
    MENU_VIEW_LABEL,
)


def create_menu_bar(window) -> QMenuBar:
    """Construct the menu bar for the JereIDE main window and bind menu events.

    Args:
        window: The MainFrame instance whose event handlers will be bound.
    
    Returns:
        The created QMenuBar instance.
    """
    menu_bar = QMenuBar()

    # ---- File menu -------------------------------------------------
    file_menu = QMenu(MENU_FILE_LABEL, menu_bar)
    new_action = file_menu.addAction(MENU_NEW_LABEL)
    open_action = file_menu.addAction(MENU_OPEN_LABEL)
    save_action = file_menu.addAction(MENU_SAVE_LABEL)
    save_as_action = file_menu.addAction(MENU_SAVE_AS_LABEL)
    file_menu.addSeparator()
    close_tab_action = file_menu.addAction(MENU_CLOSE_TAB_LABEL)

    new_action.triggered.connect(window.on_new)
    open_action.triggered.connect(window.on_open)
    save_action.triggered.connect(window.on_save)
    save_as_action.triggered.connect(window.on_save_as)
    close_tab_action.triggered.connect(window.on_close_tab)

    menu_bar.addMenu(file_menu)

    # ---- Edit menu -------------------------------------------------
    edit_menu = QMenu(MENU_EDIT_LABEL, menu_bar)
    find_action = edit_menu.addAction(MENU_FIND_LABEL)
    find_next_action = edit_menu.addAction(MENU_FIND_NEXT_LABEL)
    replace_action = edit_menu.addAction(MENU_REPLACE_LABEL)

    find_action.triggered.connect(window.on_find)
    find_next_action.triggered.connect(window.on_find_next)
    replace_action.triggered.connect(window.on_replace)

    menu_bar.addMenu(edit_menu)

    # ---- View menu -------------------------------------------------
    view_menu = QMenu(MENU_VIEW_LABEL, menu_bar)
    toggle_line_numbers_action = view_menu.addAction(MENU_TOGGLE_LINE_NUMBERS_LABEL)

    toggle_line_numbers_action.triggered.connect(window.on_toggle_line_numbers)

    menu_bar.addMenu(view_menu)

    # ---- Help menu ------------------------------------------------
    help_menu = QMenu(MENU_HELP_LABEL, menu_bar)
    about_action = help_menu.addAction(MENU_ABOUT_LABEL)

    about_action.triggered.connect(window.on_about)

    menu_bar.addMenu(help_menu)

    window.setMenuBar(menu_bar)
    return menu_bar
