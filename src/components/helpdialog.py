import wx
import wx.adv

def show_about_dialog(parent):
    """Display an About dialog for JereIDE."""
    info = wx.adv.AboutDialogInfo()
    info.SetName("JereIDE")
    info.SetVersion("Beta")
    info.SetDescription(
        "JereIDE – a minimal IDE built with wxPython.\n"
        "Features include opening, saving, and basic text editing."
    )
    info.SetCopyright("Copyright (C) 2026 Jeremy-Qian")
    wx.adv.AboutBox(info)
