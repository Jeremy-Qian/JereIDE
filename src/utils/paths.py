"""Filesystem path helpers for locating bundled resources."""
import os
import sys
from constants import ICONS_DIR_NAME

def icon_path(icon_filename: str) -> str:
    """Return the absolute path to a bundled icon file.
    
    This function handles both normal Python execution and PyInstaller bundled execution.
    For PyInstaller, it checks multiple common locations where resources might be extracted.
    """
    if not getattr(sys, 'frozen', False):
        # Normal Python execution
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(project_root, ICONS_DIR_NAME, icon_filename)
    
    # PyInstaller bundle execution - check multiple possible locations
    locations = [
        # Main application directory (where the executable is)
        os.path.join(os.path.dirname(sys.executable), ICONS_DIR_NAME, icon_filename),
        # PyInstaller temporary directory
        os.path.join(sys._MEIPASS, ICONS_DIR_NAME, icon_filename),
        # Common alternative locations
        os.path.join(sys._MEIPASS, 'src', ICONS_DIR_NAME, icon_filename),
        os.path.join(sys._MEIPASS, 'Resources', ICONS_DIR_NAME, icon_filename),
    ]
    
    # Return first location that exists
    for location in locations:
        if os.path.exists(location):
            return location
    
    # If not found, create it in the application directory
    app_icons_dir = os.path.join(os.path.dirname(sys.executable), ICONS_DIR_NAME)
    os.makedirs(app_icons_dir, exist_ok=True)
    return os.path.join(app_icons_dir, icon_filename)

def project_root() -> str:
    """Return the absolute path to the project root directory."""
    if getattr(sys, 'frozen', False):
        # In PyInstaller bundle, return the directory containing the executable
        return os.path.dirname(sys.executable)
    
    # In normal Python execution, calculate from this file's location
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))