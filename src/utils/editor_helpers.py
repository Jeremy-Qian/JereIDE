"""Editor utility functions for styling, keywords, and configuration helpers."""

import keyword


def get_editor_font_face():
    """Get the appropriate font face for the editor."""
    from constants import EDITOR_FONT_FACE
    return EDITOR_FONT_FACE


def get_editor_font_size():
    """Get the default font size for the editor."""
    from constants import EDITOR_FONT_SIZE
    return EDITOR_FONT_SIZE


def get_python_keywords_string():
    """Get Python keywords as a space-separated string for QScintilla."""
    return " ".join(keyword.kwlist)