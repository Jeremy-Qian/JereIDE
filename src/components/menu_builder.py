import wx

from constants import (
    MENU_ABOUT_LABEL,
    MENU_FILE_LABEL,
    MENU_HELP_LABEL,
    MENU_OPEN_LABEL,
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
    open_menu_item = file_menu.Append(wx.ID_OPEN, MENU_OPEN_LABEL)
    save_menu_item = file_menu.Append(wx.ID_SAVE, MENU_SAVE_LABEL)

    frame.Bind(wx.EVT_MENU, frame.on_open, open_menu_item)
    frame.Bind(wx.EVT_MENU, frame.on_save, save_menu_item)

    menu_bar.Append(file_menu, MENU_FILE_LABEL)

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
