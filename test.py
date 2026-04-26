import wx

class JereIDETab(wx.Control):
    """A single tab widget with a close button."""
    def __init__(self, parent, label, page, index):
        super().__init__(parent)
        self.label = label
        self.page = page
        self.index = index
        self.is_selected = False

        # Define 'X' button area (relative to tab)
        self.close_rect = wx.Rect(0, 0, 5, 5)

        self.SetInitialSize((120, 30))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseClick)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        w, h = self.GetSize()

        # Colors
        bg_color = wx.Colour(200, 200, 200) if not self.is_selected else wx.WHITE
        dc.SetBrush(wx.Brush(bg_color))
        dc.SetPen(wx.Pen(wx.Colour(150, 150, 150)))

        # Draw Tab Shape
        dc.DrawRectangle(0, 0, w, h)

        # Draw Text
        dc.SetTextForeground(wx.BLACK)
        dc.DrawText(self.label, 10, (h // 2) - 8)

        # Draw 'X' Close Button
        self.close_rect.SetPosition((w - 15, (h // 2) - 3))
        dc.SetPen(wx.Pen(wx.BLACK, 2))
        r = self.close_rect
        dc.DrawLine(r.x, r.y, r.x + r.width, r.y + r.height)
        dc.DrawLine(r.x + r.width, r.y, r.x, r.y + r.height)

    def OnMouseClick(self, event):
        pos = event.GetPosition()
        if self.close_rect.Contains(pos):
            # Tell the parent notebook to close this tab
            self.GetParent().CloseTab(self.index)
        else:
            # Select this tab
            self.GetParent().SelectTab(self.index)

class JereIDEBook(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.tabs = []
        self.pages = []
        self.current_selection = -1

        # Main Sizer
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Tab Bar (Horizontal Sizer)
        self.tab_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Page Container
        self.container = wx.BoxSizer(wx.VERTICAL)

        self.main_sizer.Add(self.tab_bar_sizer, 0, wx.EXPAND)
        self.main_sizer.Add(self.container, 1, wx.EXPAND)
        self.SetSizer(self.main_sizer)

    def AddPage(self, page_panel, label):
        index = len(self.tabs)
        tab = JereIDETab(self, label, page_panel, index)

        self.tabs.append(tab)
        self.pages.append(page_panel)
        self.tab_bar_sizer.Add(tab, 0, wx.RIGHT, 2)

        self.container.Add(page_panel, 1, wx.EXPAND)
        page_panel.Hide()

        if self.current_selection == -1:
            self.SelectTab(0)

        self.Layout()

    def SelectTab(self, index):
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

    def CloseTab(self, index):
        # Clean up the UI components
        tab = self.tabs.pop(index)
        page = self.pages.pop(index)

        tab.Destroy()
        page.Destroy()

        # Re-index remaining tabs
        for i, t in enumerate(self.tabs):
            t.index = i

        if self.current_selection >= len(self.tabs):
            self.current_selection = len(self.tabs) - 1

        if self.tabs:
            self.SelectTab(self.current_selection)

        self.Layout()

# --- Usage ---
class ExampleFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Hand-built Notebook", size=(400, 300))
        nb = JereIDEBook(self)

        p1 = wx.Panel(nb); p1.SetBackgroundColour("Sky Blue")
        p2 = wx.Panel(nb); p2.SetBackgroundColour("Green")

        nb.AddPage(p1, "Blue Tab")
        nb.AddPage(p2, "Green Tab")

app = wx.App()
ExampleFrame().Show()
app.MainLoop()
