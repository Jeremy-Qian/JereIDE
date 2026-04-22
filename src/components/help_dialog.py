import wx
import wx.adv

from constants import APP_COPYRIGHT, APP_DESCRIPTION, APP_NAME, APP_VERSION


def show_about_dialog(parent: wx.Window) -> None:
    """Display an About dialog for JereIDE."""
    about_info = wx.adv.AboutDialogInfo()
    about_info.SetName(APP_NAME)
    about_info.SetVersion(APP_VERSION)
    about_info.SetDescription(APP_DESCRIPTION)
    about_info.SetCopyright(APP_COPYRIGHT)
    wx.adv.AboutBox(about_info)
