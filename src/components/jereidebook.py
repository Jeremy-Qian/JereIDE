from __future__ import annotations

import wx


class JereIDETab(wx.Control):
    """A single tab widget with a close button."""

    def __init__(self, parent: wx.Window, label: str, page: wx.Window, index: int):
        super().__init__(parent)
        self.label = label
        self.page = page
        self.index = index
        self.is_selected = False

        self.close_rect = wx.Rect(0, 0, 5, 5)
        self.is_close_hovered = False
        self._close_hover_rect = wx.Rect(0, 0, 15, 15)

        self.SetInitialSize((120, 30))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseClick)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

    def OnPaint(self, event: wx.PaintEvent) -> None:
        dc = wx.PaintDC(self)
        w, h = self.GetSize()

        bg_color = wx.Colour(200, 200, 200) if not self.is_selected else wx.WHITE
        dc.SetBrush(wx.Brush(bg_color))
        dc.SetPen(wx.Pen(wx.Colour(150, 150, 150)))

        dc.DrawRectangle(0, 0, w, h)

        dc.SetTextForeground(wx.BLACK)
        dc.DrawText(self.label, 10, (h // 2) - 8)

        close_x = w - 15
        close_y = (h // 2) - 3
        self.close_rect.SetPosition((close_x, close_y))
        self._close_hover_rect.SetPosition((close_x - 5, close_y - 5))

        if self.is_close_hovered:
            dc.SetBrush(wx.Brush(wx.Colour(220, 220, 220)))
            dc.SetPen(wx.TRANSPARENT_PEN)
            r = self._close_hover_rect
            dc.DrawRoundedRectangle(r.x, r.y, r.width, r.height, 3)

        dc.SetPen(wx.Pen(wx.BLACK, 2))
        r = self.close_rect
        dc.DrawLine(r.x, r.y, r.x + r.width, r.y + r.height)
        dc.DrawLine(r.x + r.width, r.y, r.x, r.y + r.height)

    def OnMouseMove(self, event: wx.MouseEvent) -> None:
        pos = event.GetPosition()
        was_hovered = self.is_close_hovered
        self.is_close_hovered = self._close_hover_rect.Contains(pos)
        if was_hovered != self.is_close_hovered:
            self.Refresh()

    def OnLeaveWindow(self, event: wx.WindowEvent) -> None:
        self.is_close_hovered = False
        self.Refresh()

    def OnMouseClick(self, event: wx.MouseEvent) -> None:
        pos = event.GetPosition()
        if self._close_hover_rect.Contains(pos):
            self.GetParent().CloseTab(self.index)
        else:
            self.GetParent().SelectTab(self.index)


class JereIDEBook(wx.Panel):
    """A notebook widget that manages multiple tabs with closeable tab headers."""

    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.tabs: list[JereIDETab] = []
        self.pages: list[wx.Window] = []
        self.current_selection = -1

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.tab_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.container = wx.BoxSizer(wx.VERTICAL)

        self.main_sizer.Add(self.tab_bar_sizer, 0, wx.EXPAND)
        self.main_sizer.Add(self.container, 1, wx.EXPAND)
        self.SetSizer(self.main_sizer)

    def _on_page_changed(self, event: wx.CommandEvent) -> None:
        """Handle page change events."""
        if event is not None:
            event.Skip()

    def _on_page_close(self, event: wx.CommandEvent) -> None:
        """Handle page close events."""
        if event is not None:
            event.Skip()

    # API compatibility with wx.aui.AuiNotebook
    def GetSelection(self) -> int:
        """Return the currently selected page index, or wx.NOT_FOUND."""
        return self.current_selection

    def GetPage(self, index: int) -> wx.Window | None:
        """Return the page at the given index."""
        if 0 <= index < len(self.pages):
            return self.pages[index]
        return None

    def AddPage(self, page_panel: wx.Window, title: str, select: bool = False) -> bool:
        """Add a new page to the notebook.

        Args:
            page_panel: The panel to add.
            title: The title/label for the tab.
            select: Whether to select the newly added page.

        Returns:
            True if the page was added successfully.
        """
        index = len(self.tabs)
        tab = JereIDETab(self, title, page_panel, index)

        self.tabs.append(tab)
        self.pages.append(page_panel)
        self.tab_bar_sizer.Add(tab, 0, wx.RIGHT, 2)

        self.container.Add(page_panel, 1, wx.EXPAND)
        page_panel.Hide()

        if self.current_selection == -1 or select:
            self.SelectTab(index)

        self.Layout()
        return True

    def SetPageText(self, index: int, title: str) -> bool:
        """Set the title of the page at the given index."""
        if 0 <= index < len(self.tabs):
            self.tabs[index].label = title
            self.tabs[index].Refresh()
            return True
        return False

    def GetPageIndex(self, page: wx.Window) -> int:
        """Return the index of the given page, or wx.NOT_FOUND."""
        try:
            return self.pages.index(page)
        except ValueError:
            return wx.NOT_FOUND

    def SetSelection(self, index: int) -> int:
        """Set the selection to the page at the given index. Returns previous selection."""
        old_selection = self.current_selection
        self.SelectTab(index)
        return old_selection

    def GetPageCount(self) -> int:
        """Return the number of pages."""
        return len(self.pages)

    def DeletePage(self, index: int) -> None:
        """Delete the page at the given index."""
        if 0 <= index < len(self.pages):
            self.CloseTab(index)

    def SelectTab(self, index: int) -> None:
        """Select the tab at the given index.

        Args:
            index: The index of the tab to select.
        """
        for i, (tab, page) in enumerate(zip(self.tabs, self.pages)):
            if i == index:
                tab.is_selected = True
                page.Show()
                self.current_selection = i
            else:
                tab.is_selected = False
                page.Hide()
            tab.Refresh()
        self.Layout()

    def CloseTab(self, index: int) -> None:
        """Close and remove the tab at the given index.

        Args:
            index: The index of the tab to close.
        """
        tab = self.tabs.pop(index)
        page = self.pages.pop(index)

        tab.Destroy()
        page.Destroy()

        for i, t in enumerate(self.tabs):
            t.index = i

        if self.current_selection >= len(self.tabs):
            self.current_selection = len(self.tabs) - 1

        if self.tabs:
            self.SelectTab(self.current_selection)

        self.Layout()