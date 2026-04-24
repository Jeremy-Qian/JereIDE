"""Filesystem path helpers for locating bundled resources."""
import os
import sys
from constants import ICONS_DIR_NAME


def icon_path(icon_filename: str) -> str:
    """Return the absolute path to a bundled icon file.
    
    This function handles both normal Python execution and PyInstaller bundled execution.
    """
    if not getattr(sys, 'frozen', False):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(project_root, ICONS_DIR_NAME, icon_filename)
    
    return os.path.join(sys._MEIPASS, ICONS_DIR_NAME, icon_filename)


def project_root() -> str:
    """Return the absolute path to the project root directory."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))