"""File-open and file-save dialog helpers for the editor."""
import os
from dataclasses import dataclass
from typing import Optional

import wx

from constants import FILE_WILDCARDS, OPEN_DIALOG_TITLE, SAVE_DIALOG_TITLE

_FILE_ERROR_TITLE = "File Error"
_ENCODING_ERROR_TITLE = "Encoding Error"


@dataclass
class FileOperationResult:
    """Structured result from a file operation.
    
    Attributes:
        success: Whether the operation succeeded.
        path: The file path if successful, None otherwise.
        content: The file content if reading, None otherwise.
        error: Error message if failed, None otherwise.
    """
    success: bool
    path: Optional[str] = None
    content: Optional[str] = None
    error: Optional[str] = None


def _show_error_dialog(parent: wx.Window, title: str, message: str) -> None:
    """Display a modal error message box."""
    wx.MessageBox(message, title, wx.OK | wx.ICON_ERROR, parent)


def open_file(parent: wx.Window) -> FileOperationResult:
    """Show a file-open dialog and return the selected file's contents.

    Returns:
        FileOperationResult with success=True and content if successful,
        or success=False with error message on failure.
    """
    open_dialog = wx.FileDialog(
        parent, OPEN_DIALOG_TITLE, os.getcwd(), "", FILE_WILDCARDS, wx.FD_OPEN
    )

    result = FileOperationResult(success=False)
    try:
        if open_dialog.ShowModal() != wx.ID_OK:
            return result

        selected_path = open_dialog.GetPath()

        # Check if file exists and is readable
        if not os.path.exists(selected_path):
            _show_error_dialog(
                parent,
                _FILE_ERROR_TITLE,
                f"File not found: {selected_path}",
            )
            result.error = f"File not found: {selected_path}"
            return result

        if not os.access(selected_path, os.R_OK):
            _show_error_dialog(
                parent,
                _FILE_ERROR_TITLE,
                f"Permission denied: {selected_path}\n"
                "You do not have read permissions for this file.",
            )
            result.error = f"Permission denied: {selected_path}"
            return result

        # Attempt to read the file with specific error handling
        try:
            with open(selected_path, "r", encoding="utf-8") as source_file:
                file_content = source_file.read()
            result = FileOperationResult(success=True, path=selected_path, content=file_content)
        except UnicodeDecodeError as decode_error:
            _show_error_dialog(
                parent,
                _ENCODING_ERROR_TITLE,
                f"Error reading file: {selected_path}\n"
                f"The file contains characters that cannot be decoded as UTF-8.\n"
                f"UnicodeDecodeError: {decode_error}",
            )
            result.error = f"Unicode decode error in {selected_path}"
        except PermissionError:
            _show_error_dialog(
                parent,
                _FILE_ERROR_TITLE,
                f"Permission denied: {selected_path}\n"
                "You do not have read permissions for this file.",
            )
            result.error = f"Permission denied: {selected_path}"
        except FileNotFoundError:
            _show_error_dialog(
                parent,
                _FILE_ERROR_TITLE,
                f"File not found: {selected_path}",
            )
            result.error = f"File not found: {selected_path}"
        except OSError as os_error:
            _show_error_dialog(
                parent,
                _FILE_ERROR_TITLE,
                f"Error reading file: {selected_path}\n"
                f"OS Error: {os_error.strerror} (errno {os_error.errno})",
            )
            result.error = f"OS Error: {os_error.strerror}"
    finally:
        open_dialog.Destroy()

    return result


def save_file(
    parent: wx.Window, current_path: Optional[str], content: str
) -> FileOperationResult:
    """Save ``content`` to ``current_path``, prompting for a path if needed.

    Args:
        parent: Parent window for modal dialogs.
        current_path: The file's existing path, or ``None`` to trigger a
            "Save As" prompt.
        content: The text to write.

    Returns:
        FileOperationResult with success=True and path if saved successfully,
        or success=False with error message on failure.
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
                return FileOperationResult(success=False)
            target_path = save_dialog.GetPath()
        finally:
            save_dialog.Destroy()

    # Check directory permissions
    target_directory = os.path.dirname(target_path)
    if target_directory and not os.access(target_directory, os.W_OK):
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Cannot save to: {target_directory}\n"
            "You may not have write permissions for this directory.",
        )
        return FileOperationResult(
            success=False,
            error=f"Permission denied: cannot write to {target_directory}"
        )

    # Attempt to save the file with specific error handling
    try:
        with open(target_path, "w", encoding="utf-8") as destination_file:
            destination_file.write(content)
        return FileOperationResult(success=True, path=target_path)
    except PermissionError:
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Permission denied: {target_path}\n"
            "You do not have write permissions for this file.",
        )
        return FileOperationResult(
            success=False,
            error=f"Permission denied: {target_path}"
        )
    except FileNotFoundError:
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Directory not found: {target_directory}\n"
            "The parent directory does not exist.",
        )
        return FileOperationResult(
            success=False,
            error=f"Directory not found: {target_directory}"
        )
    except OSError as os_error:
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Error saving file: {target_path}\n"
            f"OS Error: {os_error.strerror} (errno {os_error.errno})",
        )
        return FileOperationResult(
            success=False,
            error=f"OS Error: {os_error.strerror}"
        )