"""Filesystem path helpers for locating bundled resources."""
import os
import sys

from constants import ICONS_DIR_NAME

# This file lives at: <project_root>/src/utils/paths.py
# `<project_root>` is the directory that contains `src/` and `icons/`.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def project_root() -> str:
    """Return the absolute path to the project root directory."""
    return _PROJECT_ROOT


def icon_path(icon_filename: str) -> str:
    """Return the absolute path to a bundled icon file."""
    return os.path.join(_PROJECT_ROOT, ICONS_DIR_NAME, icon_filename)
