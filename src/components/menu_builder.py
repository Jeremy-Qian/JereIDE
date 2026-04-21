import wx
from constants import *

def create_menu_bar(frame):
    """
    Constructs the menu bar for the JereIDE main frame and binds menu events.

    Args:
        frame: The MainFrame instance to which the menu bar will be attached
               and whose event handlers will be bound.
    """
    menu_bar = wx.MenuBar()

    # ---- File menu -------------------------------------------------
    file_menu = wx.Menu()
    open_item = file_menu.Append(
        wx.ID_OPEN, MENU_OPEN_LABEL)
    save_item = file_menu.Append(
        wx.ID_SAVE, MENU_SAVE_LABEL)

    # Bind menu events to the frame's methods
    frame.Bind(wx.EVT_MENU, frame.on_open, open_item)
    frame.Bind(wx.EVT_MENU, frame.on_save, save_item)

    menu_bar.Append(file_menu, MENU_FILE_LABEL)

    # ---- View menu -------------------------------------------------
    view_menu = wx.Menu()
    toggle_line_numbers_item = view_menu.Append(
        wx.ID_ANY, MENU_TOGGLE_LINE_NUMBERS_LABEL)

    # Bind menu events to the frame's methods
    frame.Bind(wx.EVT_MENU, frame.on_toggle_line_numbers, toggle_line_numbers_item)

    menu_bar.Append(view_menu, MENU_VIEW_LABEL)

    # ---- Help menu ------------------------------------------------
    help_menu = wx.Menu()
    about_item = help_menu.Append(
        wx.ID_ABOUT, MENU_ABOUT_LABEL)

    # Bind menu event to the frame's method
    frame.Bind(wx.EVT_MENU, frame.on_about, about_item)

    menu_bar.Append(help_menu, MENU_HELP_LABEL)

    frame.SetMenuBar(menu_bar)
