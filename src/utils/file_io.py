import wx
import os
from constants import *

def open_file(parent):
    """
    Shows a file open dialog and returns the path and content of the selected file.
    Returns (path, content) if successful, (None, None) otherwise.
    """
    dialog = wx.FileDialog(
        parent, OPEN_DIALOG_TITLE, os.getcwd(), "", FILE_WILDCARDS, wx.FD_OPEN
    )

    result = (None, None)

    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()

        # Validate that file is readable
        if not os.access(path, os.R_OK):
            wx.MessageBox(
                f"Cannot open file: {path}\n"
                "The file may not exist or you may not have read permissions.",
                "File Error",
                wx.OK | wx.ICON_ERROR,
                parent
            )
        else:
            try:
                with open(path, "r", encoding='utf-8') as file:
                    content = file.read()
                    result = (path, content)
            except IOError as e:
                wx.MessageBox(
                    f"Error reading file: {path}\n"
                    f"IOError: {str(e)}",
                    "File Error",
                    wx.OK | wx.ICON_ERROR,
                    parent
                )
            except UnicodeDecodeError as e:
                wx.MessageBox(
                    f"Error reading file: {path}\n"
                    f"The file contains characters that cannot be decoded as UTF-8.\n"
                    f"UnicodeDecodeError: {str(e)}",
                    "Encoding Error",
                    wx.OK | wx.ICON_ERROR,
                    parent
                )
            except Exception as e:
                wx.MessageBox(
                    f"Unexpected error reading file: {path}\n"
                    f"Error: {str(e)}",
                    "File Error",
                    wx.OK | wx.ICON_ERROR,
                    parent
                )

    dialog.Destroy()
    return result

def save_file(parent, path, content):
    """
    Saves the content to the given path. If path is None, prompts for a new path.
    Returns the path if saved successfully, None otherwise.
    """
    if not path:
        dialog = wx.FileDialog(
            parent,
            SAVE_DIALOG_TITLE,
            os.getcwd(),
            "",
            FILE_WILDCARDS,
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        else:
            dialog.Destroy()
            return None
        dialog.Destroy()

    # Validate that the directory is writable
    save_dir = os.path.dirname(path)
    if not os.access(save_dir, os.W_OK):
        wx.MessageBox(
            f"Cannot save to: {save_dir}\n"
            "You may not have write permissions for this directory.",
            "File Error",
            wx.OK | wx.ICON_ERROR,
            parent
        )
        return None

    try:
        with open(path, "w", encoding='utf-8') as file:
            file.write(content)
        return path
    except Exception as e:
        wx.MessageBox(
            f"Error saving file: {path}\n"
            f"Error: {str(e)}",
            "File Error",
            wx.OK | wx.ICON_ERROR,
            parent
        )
        return None
