"""Find/Replace dialog component for JereIDE."""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox
from PySide6.QtGui import QTextDocument


class FindDialog(QDialog):
    """A dialog for finding text in the editor."""

    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor
        self._last_search_text = ""
        self._search_flags = 0
        self._init_ui()
        self.setWindowTitle("Find")

    def _init_ui(self) -> None:
        """Initialize the dialog UI components."""
        layout = QVBoxLayout(self)

        # Find label and text box
        find_label = QLabel("Find:")
        self.find_text = QLineEdit()
        self.find_text.setFocus()
        layout.addWidget(find_label)
        layout.addWidget(self.find_text)

        # Options checkboxes
        options_layout = QHBoxLayout()
        self.match_case_checkbox = QCheckBox("Match case")
        self.match_word_checkbox = QCheckBox("Match whole word")
        options_layout.addWidget(self.match_case_checkbox)
        options_layout.addWidget(self.match_word_checkbox)
        layout.addLayout(options_layout)

        # Buttons
        button_layout = QHBoxLayout()
        find_next_btn = QPushButton("Find Next")
        find_next_btn.clicked.connect(self.on_find_next)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(find_next_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

        # Bind enter key to find next
        self.find_text.returnPressed.connect(self.on_find_next)

    def on_find_next(self) -> None:
        """Handle Find Next button click."""
        find_text = self.find_text.text()

        if not find_text:
            QMessageBox.information(self, "Find", "Please enter text to find.")
            return

        # Use Qt's built-in find
        flags = QTextDocument.FindFlags()
        if self.match_case_checkbox.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.match_word_checkbox.isChecked():
            flags |= QTextDocument.FindWholeWords

        if self.editor.find(find_text, flags):
            return  # Found
        
        # Try wrapping around
        cursor = self.editor.textCursor()
        cursor.setPosition(0)
        self.editor.setTextCursor(cursor)
        
        if self.editor.find(find_text, flags):
            return  # Found
        
        QMessageBox.information(self, "Find", f'"{find_text}" not found.')


class ReplaceDialog(QDialog):
    """A dialog for finding and replacing text in the editor."""

    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor
        self._last_search_text = ""
        self._search_flags = 0
        self._init_ui()
        self.setWindowTitle("Find and Replace")

    def _init_ui(self) -> None:
        """Initialize the dialog UI components."""
        layout = QVBoxLayout(self)

        # Find label and text box
        find_label = QLabel("Find:")
        self.find_text = QLineEdit()
        self.find_text.setFocus()
        layout.addWidget(find_label)
        layout.addWidget(self.find_text)

        # Replace label and text box
        replace_label = QLabel("Replace with:")
        self.replace_text = QLineEdit()
        layout.addWidget(replace_label)
        layout.addWidget(self.replace_text)

        # Options checkboxes
        options_layout = QHBoxLayout()
        self.match_case_checkbox = QCheckBox("Match case")
        self.match_word_checkbox = QCheckBox("Match whole word")
        options_layout.addWidget(self.match_case_checkbox)
        options_layout.addWidget(self.match_word_checkbox)
        layout.addLayout(options_layout)

        # Buttons
        button_layout = QHBoxLayout()
        replace_btn = QPushButton("Replace")
        replace_btn.clicked.connect(self.on_replace)
        replace_all_btn = QPushButton("Replace All")
        replace_all_btn.clicked.connect(self.on_replace_all)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(replace_btn)
        button_layout.addWidget(replace_all_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

        # Bind enter key to replace
        self.find_text.returnPressed.connect(self.on_replace)

    def on_replace(self) -> None:
        """Handle Replace button click."""
        find_text = self.find_text.text()
        replace_text = self.replace_text.text()

        if not find_text:
            QMessageBox.information(self, "Replace", "Please enter text to find.")
            return

        # Get current selection and check if it matches
        if self.editor.textCursor().selectedText() == find_text:
            self.editor.textCursor().insertText(replace_text)

        # Find next occurrence
        self.on_find_next()

    def on_find_next(self) -> None:
        """Handle Find Next button click."""
        find_text = self.find_text.text()

        if not find_text:
            QMessageBox.information(self, "Find", "Please enter text to find.")
            return

        flags = QTextDocument.FindFlags()
        if self.match_case_checkbox.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.match_word_checkbox.isChecked():
            flags |= QTextDocument.FindWholeWords

        if self.editor.find(find_text, flags):
            return  # Found
        
        # Try wrapping around
        cursor = self.editor.textCursor()
        cursor.setPosition(0)
        self.editor.setTextCursor(cursor)
        
        if self.editor.find(find_text, flags):
            return  # Found
        
        QMessageBox.information(self, "Find", f'"{find_text}" not found.')

    def on_replace_all(self) -> None:
        """Handle Replace All button click."""
        from PySide6.QtGui import QTextCursor
        
        find_text = self.find_text.text()
        replace_text = self.replace_text.text()

        if not find_text:
            QMessageBox.information(self, "Replace", "Please enter text to find.")
            return

        replacements = 0
        cursor = self.editor.textCursor()
        cursor.setPosition(0)
        self.editor.setTextCursor(cursor)
        
        flags = QTextDocument.FindFlags()
        if self.match_case_checkbox.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.match_word_checkbox.isChecked():
            flags |= QTextDocument.FindWholeWords
        
        while self.editor.find(find_text, flags):
            self.editor.textCursor().insertText(replace_text)
            replacements += 1

        QMessageBox.information(self, "Replace All", f"Replaced {replacements} occurrence(s).")