"""File-open and file-save dialog helpers for the editor."""
import os
from typing import Optional, Tuple

import wx

from constants import FILE_WILDCARDS, OPEN_DIALOG_TITLE, SAVE_DIALOG_TITLE

_FILE_ERROR_TITLE = "File Error"
_ENCODING_ERROR_TITLE = "Encoding Error"


def _show_error_dialog(parent: wx.Window, title: str, message: str) -> None:
    """Display a modal error message box."""
    wx.MessageBox(message, title, wx.OK | wx.ICON_ERROR, parent)


def open_file(parent: wx.Window) -> Tuple[Optional[str], Optional[str]]:
    """Show a file-open dialog and return the selected file's path and contents.

    Returns:
        ``(path, content)`` if a file was selected and read successfully,
        otherwise ``(None, None)``.
    """
    open_dialog = wx.FileDialog(
        parent, OPEN_DIALOG_TITLE, os.getcwd(), "", FILE_WILDCARDS, wx.FD_OPEN
    )

    result: Tuple[Optional[str], Optional[str]] = (None, None)
    try:
        if open_dialog.ShowModal() != wx.ID_OK:
            return result

        selected_path = open_dialog.GetPath()

        if not os.access(selected_path, os.R_OK):
            _show_error_dialog(
                parent,
                _FILE_ERROR_TITLE,
                f"Cannot open file: {selected_path}\n"
                "The file may not exist or you may not have read permissions.",
            )
            return result

        try:
            with open(selected_path, "r", encoding="utf-8") as source_file:
                file_content = source_file.read()
            result = (selected_path, file_content)
        except UnicodeDecodeError as decode_error:
            _show_error_dialog(
                parent,
                _ENCODING_ERROR_TITLE,
                f"Error reading file: {selected_path}\n"
                f"The file contains characters that cannot be decoded as UTF-8.\n"
                f"UnicodeDecodeError: {decode_error}",
            )
        except IOError as io_error:
            _show_error_dialog(
                parent,
                _FILE_ERROR_TITLE,
                f"Error reading file: {selected_path}\nIOError: {io_error}",
            )
        except Exception as unexpected_error:  # noqa: BLE001 - surface any failure to the user
            _show_error_dialog(
                parent,
                _FILE_ERROR_TITLE,
                f"Unexpected error reading file: {selected_path}\n"
                f"Error: {unexpected_error}",
            )
    finally:
        open_dialog.Destroy()

    return result


def save_file(
    parent: wx.Window, current_path: Optional[str], content: str
) -> Optional[str]:
    """Save ``content`` to ``current_path``, prompting for a path if needed.

    Args:
        parent: Parent window for modal dialogs.
        current_path: The file's existing path, or ``None`` to trigger a
            "Save As" prompt.
        content: The text to write.

    Returns:
        The path the file was saved to, or ``None`` if the user cancelled or
        the save failed.
    """
    target_path = current_path
    if not target_path:
        save_dialog = wx.FileDialog(
            parent,
            SAVE_DIALOG_TITLE,
            os.getcwd(),
            "",
            FILE_WILDCARDS,
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )
        try:
            if save_dialog.ShowModal() != wx.ID_OK:
                return None
            target_path = save_dialog.GetPath()
        finally:
            save_dialog.Destroy()

    target_directory = os.path.dirname(target_path)
    if not os.access(target_directory, os.W_OK):
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Cannot save to: {target_directory}\n"
            "You may not have write permissions for this directory.",
        )
        return None

    try:
        with open(target_path, "w", encoding="utf-8") as destination_file:
            destination_file.write(content)
        return target_path
    except Exception as save_error:  # noqa: BLE001 - surface any failure to the user
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Error saving file: {target_path}\nError: {save_error}",
        )
        return None
