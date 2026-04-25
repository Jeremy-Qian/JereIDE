import wx

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


def create_menu_bar(frame: wx.Frame) -> None:
    """Construct the menu bar for the JereIDE main frame and bind menu events.

    Args:
        frame: The MainFrame instance to which the menu bar will be attached
            and whose event handlers will be bound.
    """
    menu_bar = wx.MenuBar()

    # ---- File menu -------------------------------------------------
    file_menu = wx.Menu()
    new_menu_item = file_menu.Append(wx.ID_NEW, MENU_NEW_LABEL)
    open_menu_item = file_menu.Append(wx.ID_OPEN, MENU_OPEN_LABEL)
    save_menu_item = file_menu.Append(wx.ID_SAVE, MENU_SAVE_LABEL)
    save_as_menu_item = file_menu.Append(wx.ID_SAVEAS, MENU_SAVE_AS_LABEL)
    file_menu.AppendSeparator()
    close_tab_menu_item = file_menu.Append(wx.ID_CLOSE, MENU_CLOSE_TAB_LABEL)

    frame.Bind(wx.EVT_MENU, frame.on_new, new_menu_item)
    frame.Bind(wx.EVT_MENU, frame.on_open, open_menu_item)
    frame.Bind(wx.EVT_MENU, frame.on_save, save_menu_item)
    frame.Bind(wx.EVT_MENU, frame.on_save_as, save_as_menu_item)
    frame.Bind(wx.EVT_MENU, frame.on_close_tab, close_tab_menu_item)

    menu_bar.Append(file_menu, MENU_FILE_LABEL)

    # ---- Edit menu -------------------------------------------------
    edit_menu = wx.Menu()
    # edit_menu.Append(wx.ID_ANY, "Undo")
    # edit_menu.Append(wx.ID_ANY, "Redo")
    # edit_menu.Append(wx.ID_ANY, "Cut")
    # edit_menu.Append(wx.ID_ANY, "Copy")
    # edit_menu.Append(wx.ID_ANY, "Paste")

    edit_menu.AppendSeparator()
    find_menu_item = edit_menu.Append(wx.ID_ANY, MENU_FIND_LABEL)
    find_next_menu_item = edit_menu.Append(wx.ID_ANY, MENU_FIND_NEXT_LABEL)
    replace_menu_item = edit_menu.Append(wx.ID_ANY, MENU_REPLACE_LABEL)

    frame.Bind(wx.EVT_MENU, frame.on_find, find_menu_item)
    frame.Bind(wx.EVT_MENU, frame.on_find_next, find_next_menu_item)
    frame.Bind(wx.EVT_MENU, frame.on_replace, replace_menu_item)

    menu_bar.Append(edit_menu, MENU_EDIT_LABEL)

    # ---- View menu -------------------------------------------------
    view_menu = wx.Menu()
    toggle_line_numbers_menu_item = view_menu.Append(
        wx.ID_ANY, MENU_TOGGLE_LINE_NUMBERS_LABEL
    )

    frame.Bind(
        wx.EVT_MENU, frame.on_toggle_line_numbers, toggle_line_numbers_menu_item
    )

    menu_bar.Append(view_menu, MENU_VIEW_LABEL)

    # ---- Help menu ------------------------------------------------
    help_menu = wx.Menu()
    about_menu_item = help_menu.Append(wx.ID_ABOUT, MENU_ABOUT_LABEL)

    frame.Bind(wx.EVT_MENU, frame.on_about, about_menu_item)

    menu_bar.Append(help_menu, MENU_HELP_LABEL)

    frame.SetMenuBar(menu_bar)
