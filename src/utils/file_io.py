"""File-open and file-save dialog helpers for the editor."""
import os
from dataclasses import dataclass
from typing import Optional

from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget

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


def _show_error_dialog(parent: QWidget, title: str, message: str) -> None:
    """Display a modal error message box."""
    QMessageBox.critical(parent, title, message)


def open_file(parent: QWidget) -> FileOperationResult:
    """Show a file-open dialog and return the selected file's contents.

    Returns:
        FileOperationResult with success=True and content if successful,
        or success=False with error message on failure.
    """
    file_path, _ = QFileDialog.getOpenFileName(
        parent, OPEN_DIALOG_TITLE, os.getcwd(), FILE_WILDCARDS
    )

    if not file_path:
        return FileOperationResult(success=False)

    # Check if file exists and is readable
    if not os.path.exists(file_path):
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"File not found: {file_path}"
        )
        return FileOperationResult(success=False, error=f"File not found: {file_path}")

    if not os.access(file_path, os.R_OK):
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Permission denied: {file_path}\nYou do not have read permissions for this file."
        )
        return FileOperationResult(success=False, error=f"Permission denied: {file_path}")

    # Attempt to read the file with specific error handling
    try:
        with open(file_path, "r", encoding="utf-8") as source_file:
            file_content = source_file.read()
        return FileOperationResult(success=True, path=file_path, content=file_content)
    except UnicodeDecodeError as decode_error:
        _show_error_dialog(
            parent,
            _ENCODING_ERROR_TITLE,
            f"Error reading file: {file_path}\n"
            f"The file contains characters that cannot be decoded as UTF-8.\n"
            f"UnicodeDecodeError: {decode_error}"
        )
        return FileOperationResult(success=False, error=f"Unicode decode error in {file_path}")
    except PermissionError:
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Permission denied: {file_path}\nYou do not have read permissions for this file."
        )
        return FileOperationResult(success=False, error=f"Permission denied: {file_path}")
    except FileNotFoundError:
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"File not found: {file_path}"
        )
        return FileOperationResult(success=False, error=f"File not found: {file_path}")
    except OSError as os_error:
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Error reading file: {file_path}\nOS Error: {os_error.strerror} (errno {os_error.errno})"
        )
        return FileOperationResult(success=False, error=f"OS Error: {os_error.strerror}")


def save_file(
    parent: QWidget, current_path: Optional[str], content: str
) -> FileOperationResult:
    """Save ``content`` to ``current_path``, prompting for a path if needed.

    Args:
        parent: Parent widget for modal dialogs.
        current_path: The file's existing path, or ``None`` to trigger a
            "Save As" prompt.
        content: The text to write.

    Returns:
        FileOperationResult with success=True and path if saved successfully,
        or success=False with error message on failure.
    """
    target_path = current_path
    if not target_path:
        target_path, _ = QFileDialog.getSaveFileName(
            parent,
            SAVE_DIALOG_TITLE,
            os.getcwd(),
            FILE_WILDCARDS
        )
        if not target_path:
            return FileOperationResult(success=False)

    # Check directory permissions
    target_directory = os.path.dirname(target_path)
    if target_directory and not os.access(target_directory, os.W_OK):
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Cannot save to: {target_directory}\nYou may not have write permissions for this directory."
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
            f"Permission denied: {target_path}\nYou do not have write permissions for this file."
        )
        return FileOperationResult(
            success=False,
            error=f"Permission denied: {target_path}"
        )
    except FileNotFoundError:
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Directory not found: {target_directory}\nThe parent directory does not exist."
        )
        return FileOperationResult(
            success=False,
            error=f"Directory not found: {target_directory}"
        )
    except OSError as os_error:
        _show_error_dialog(
            parent,
            _FILE_ERROR_TITLE,
            f"Error saving file: {target_path}\nOS Error: {os_error.strerror} (errno {os_error.errno})"
        )
        return FileOperationResult(
            success=False,
            error=f"OS Error: {os_error.strerror}"
        )