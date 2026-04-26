"""Editor widget using QPlainTextEdit for basic text editing."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QTextCursor
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit

from constants import (
    EDITOR_FONT_SIZE,
    EDITOR_FONT_FACE,
    LINE_NUMBER_MARGIN_PADDING_PX,
    EDITOR_INDENT_SIZE,
    EDITOR_TAB_WIDTH,
    EDITOR_USE_TABS,
    EDITOR_FG_COLOR_DEFAULT,
    EDITOR_BG_COLOR_DEFAULT,
    EDITOR_FG_COLOR_LINENUMBER,
    EDITOR_BG_COLOR_LINENUMBER,
    EDITOR_CARET_COLOR,
    EDITOR_SELECTION_COLOR,
    EDITOR_FG_COLOR_KEYWORD,
    EDITOR_FG_COLOR_COMMENT,
    EDITOR_FG_COLOR_STRING,
    EDITOR_FG_COLOR_NUMBER,
)


class LineNumberArea(QWidget):
    """Widget that displays line numbers alongside the editor."""

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return self.editor.document().pageSize()

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class Editor(QPlainTextEdit):
    """A code editor widget with basic syntax highlighting."""

    def __init__(self, parent=None, file_path: str | None = None):
        super().__init__(parent)
        self.file_path = file_path
        self.line_numbers_enabled = True
        self._setup_editor()

    def _setup_editor(self) -> None:
        """Set up the editor with font and basic configuration."""
        font = QFont(EDITOR_FONT_FACE, EDITOR_FONT_SIZE)
        self.setFont(font)

        # Set background and foreground colors
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {EDITOR_BG_COLOR_DEFAULT};
                color: {EDITOR_FG_COLOR_DEFAULT};
                border: none;
            }}
        """)

        # Tab settings
        self.setTabChangesFocus(False)
        self.setTabStopDistance(EDITOR_TAB_WIDTH * self.fontMetrics().horizontalAdvance(' '))
        
        # Indentation
        self.setIndentWidth(EDITOR_INDENT_SIZE)

        # Line number area
        self._line_number_area = LineNumberArea(self)
        self._update_line_number_width()
        self.blockCountChanged.connect(self._update_line_number_width)
        self.updateRequest.connect(self._update_line_number_area)

        # Caret
        self.setCursorWidth(2)

        # Syntax highlighting timer
        self.textChanged.connect(self._apply_syntax_highlighting)

    def _update_line_number_width(self) -> None:
        """Update the width of the line number area."""
        if not self.line_numbers_enabled:
            self.setViewportMargins(0, 0, 0, 0)
            return

        digit_count = len(str(self.document().blockCount()))
        font_metrics = self.fontMetrics()
        width = font_metrics.horizontalAdvance('9' * digit_count) + LINE_NUMBER_MARGIN_PADDING_PX * 2
        self.setViewportMargins(width, 0, 0, 0)

    def _update_line_number_area(self, rect, dy) -> None:
        """Update the line number area when the editor scrolls."""
        if dy:
            self._line_number_area.scroll(0, dy)
        else:
            self._line_number_area.update(0, rect.y(), self._line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self._update_line_number_width()

    def line_number_area_paint_event(self, event) -> None:
        """Paint the line numbers."""
        painter = QColor(EDITOR_FG_COLOR_LINENUMBER)
        painter = QColor(EDITOR_FG_COLOR_LINENUMBER)
        bg_color = QColor(EDITOR_BG_COLOR_LINENUMBER)
        
        painter.setPen(QColor(EDITOR_FG_COLOR_LINENUMBER))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter_number = str(block_number + 1)
                painter.setPen(QColor(EDITOR_FG_COLOR_LINENUMBER))
                self._line_number_area.setStyleSheet(f"background-color: {EDITOR_BG_COLOR_LINENUMBER}; color: {EDITOR_FG_COLOR_LINENUMBER};")
                self._line_number_area.update()
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def resizeEvent(self, event) -> None:
        """Handle resize events to keep line numbers aligned."""
        super().resizeEvent(event)
        if self.line_numbers_enabled:
            cr = self.contentsRect()
            self._line_number_area.setGeometry(cr.left(), cr.top(), self._get_line_number_width(), cr.height())

    def _get_line_number_width(self) -> int:
        """Get the width of the line number area."""
        if not self.line_numbers_enabled:
            return 0
        digit_count = len(str(self.document().blockCount()))
        return self.fontMetrics().horizontalAdvance('9' * digit_count) + LINE_NUMBER_MARGIN_PADDING_PX * 2

    def set_value(self, value: str) -> None:
        """Set the text content of the editor."""
        self.setPlainText(value)
        self.setModified(False)

    def set_editable(self, is_editable: bool) -> None:
        """Set whether the editor is editable."""
        self.setReadOnly(not is_editable)

    def is_modified(self) -> bool:
        """Return whether the document has been modified."""
        return self.document().isModified()

    def clear_content(self) -> None:
        """Clear the editor content."""
        self.clear()

    def set_insertion_point(self, position: int) -> None:
        """Move the cursor to the given position."""
        cursor = self.textCursor()
        cursor.setPosition(position)
        self.setTextCursor(cursor)

    def show_position(self, position: int) -> None:
        """Scroll to show the given position."""
        cursor = self.textCursor()
        cursor.setPosition(position)
        self.setTextCursor(cursor)
        self.centerCursor()

    def get_last_position(self) -> int:
        """Return the last position in the document."""
        return self.document().characterCount()

    def get_position_from_line(self, line_number: int) -> int:
        """Get the position at the start of the given line."""
        cursor = QTextCursor(self.document().findBlockByLineNumber(line_number - 1))
        return cursor.position()

    def get_text_range(self, start_position: int, end_position: int) -> str:
        """Get text in the given range."""
        cursor = self.textCursor()
        cursor.setPosition(start_position)
        cursor.setPosition(end_position, QTextCursor.MoveMode.KeepAnchor)
        return cursor.selectedText()

    def get_selection_range(self) -> tuple:
        """Return (start, end) of the current selection."""
        cursor = self.textCursor()
        return cursor.selectionStart(), cursor.selectionEnd()

    def set_selection_range(self, start_position: int, end_position: int) -> None:
        """Select text in the given range."""
        cursor = self.textCursor()
        cursor.setPosition(start_position)
        cursor.setPosition(end_position, QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)

    def select_line(self, line_number: int) -> None:
        """Select the entire line at the given line number."""
        cursor = QTextCursor(self.document().findBlockByLineNumber(line_number - 1))
        cursor.select(QTextCursor.SelectionType.LineUnderSelection)
        self.setTextCursor(cursor)

    def goto_line(self, line_number: int) -> None:
        """Go to the given line number."""
        cursor = QTextCursor(self.document().findBlockByLineNumber(line_number - 1))
        self.setTextCursor(cursor)
        self.centerCursor()

    def register_modified_event(self, event_handler) -> None:
        """Connect the textChanged signal to the handler."""
        self.textChanged.connect(event_handler)

    def _apply_syntax_highlighting(self) -> None:
        """Apply basic syntax highlighting to the document."""
        # Basic highlighting - could be extended with a proper highlighter
        pass

    def update_line_number_margin(self) -> None:
        """Update the line number margin width."""
        self._update_line_number_width()

    def toggle_line_numbers(self) -> None:
        """Toggle line number visibility."""
        self.line_numbers_enabled = not self.line_numbers_enabled
        self._update_line_number_width()
        if not self.line_numbers_enabled:
            self.setViewportMargins(0, 0, 0, 0)
