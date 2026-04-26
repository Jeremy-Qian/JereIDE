"""Notebook widget for managing multiple tabs."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTabWidget, QWidget, QLabel, QHBoxLayout, QPushButton, QStyle


class TabLabel(QWidget):
    """A custom tab label with a close button."""
    
    closed = Signal(int)
    
    def __init__(self, title: str, index: int, parent=None):
        super().__init__(parent)
        self.index = index
        self._setup_ui(title)
    
    def _setup_ui(self, title: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        self.label = QLabel(title)
        layout.addWidget(self.label)
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(16, 16)
        self.close_btn.setStyleSheet("border: none; font-size: 14px; font-weight: bold;")
        self.close_btn.clicked.connect(lambda: self.closed.emit(self.index))
        layout.addWidget(self.close_btn)
    
    def set_title(self, title: str):
        self.label.setText(title)


class JereIDEBook(QTabWidget):
    """A notebook widget that manages multiple tabs with closeable tab headers."""
    
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setTabBar(AutoCloseTabBar(self))
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self._on_tab_close_requested)
        
        # Create a placeholder widget when empty
        self._empty_widget = QWidget()
    
    def add_tab(self, title: str, widget: QWidget) -> int:
        """Add a new tab with the given title and widget."""
        idx = super().addTab(widget, title)
        return idx
    
    def set_tab_text(self, index: int, title: str) -> None:
        """Set the title of the tab at the given index."""
        if 0 <= index < self.count():
            self.setTabText(index, title)
    
    def get_current_editor(self):
        """Return the currently selected editor widget."""
        return self.currentWidget()
    
    def _on_tab_close_requested(self, index: int) -> None:
        """Handle tab close requests."""
        widget = self.widget(index)
        if widget is not None:
            widget.deleteLater()
        self.removeTab(index)


class AutoCloseTabBar(QTabBar):
    """Custom tab bar that tracks which tabs should have close buttons."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._closeable_tabs = set()
    
    def setTabCloseable(self, index: int, closeable: bool) -> None:
        """Set whether a tab is closeable."""
        if closeable:
            self._closeable_tabs.add(index)
        else:
            self._closeable_tabs.discard(index)
        self.update()
    
    def tabCloseable(self, index: int) -> bool:
        """Return whether a tab is closeable."""
        return index in self._closeable_tabs