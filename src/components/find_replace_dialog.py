"""Find/Replace dialog component for JereIDE."""

import wx
import wx.stc


class FindReplaceDialog(wx.Dialog):
    """A dialog for finding and replacing text in the editor."""

    def __init__(
        self,
        parent: wx.Window,
        editor: wx.stc.StyledTextCtrl,
        mode: str = "find",
    ):
        """Initialize the Find/Replace dialog.

        Args:
            parent: The parent window.
            editor: The StyledTextCtrl editor to search in.
            mode: "find" for Find only, "replace" for Find and Replace.
        """
        super().__init__(
            parent,
            title="Find" if mode == "find" else "Find and Replace",
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self.editor = editor
        self.mode = mode
        self._last_search_text = ""
        self._last_replace_text = ""
        self._search_flags = 0  # wx.stc.STC_FIND_* flags
        self._init_ui()
        self.Centre()
        self.ShowModal()
        self.Destroy()

    def _init_ui(self) -> None:
        """Initialize the dialog UI components."""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Find text box
        find_label = wx.StaticText(self, label="Find:")
        find_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.find_textCtrl = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.find_textCtrl.SetFocus()
        find_sizer.Add(self.find_textCtrl, proportion=1, flag=wx.EXPAND)

        main_sizer.Add(find_label, flag=wx.TOP | wx.LEFT, border=10)
        main_sizer.Add(find_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Replace text box (only for replace mode)
        if self.mode == "replace":
            replace_label = wx.StaticText(self, label="Replace with:")
            replace_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.replace_textCtrl = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
            replace_sizer.Add(self.replace_textCtrl, proportion=1, flag=wx.EXPAND)

            main_sizer.Add(replace_label, flag=wx.TOP | wx.LEFT, border=10)
            main_sizer.Add(replace_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Options checkboxes
        options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.match_case_checkbox = wx.CheckBox(self, label="Match case")
        self.match_word_checkbox = wx.CheckBox(self, label="Match whole word")
        options_sizer.Add(self.match_case_checkbox)
        options_sizer.Add(self.match_word_checkbox, flag=wx.LEFT, border=10)

        main_sizer.Add(options_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Buttons
        button_sizer = wx.StdDialogButtonSizer()

        if self.mode == "find":
            find_next_btn = wx.Button(self, label="Find Next")
            find_next_btn.Bind(wx.EVT_BUTTON, self.on_find_next)
            button_sizer.AddButton(find_next_btn)
        else:
            replace_btn = wx.Button(self, label="Replace")
            replace_btn.Bind(wx.EVT_BUTTON, self.on_replace)
            button_sizer.AddButton(replace_btn)

            replace_all_btn = wx.Button(self, label="Replace All")
            replace_all_btn.Bind(wx.EVT_BUTTON, self.on_replace_all)
            button_sizer.AddButton(replace_all_btn)

        close_btn = wx.Button(self, wx.ID_CLOSE)
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        button_sizer.AddButton(close_btn)

        button_sizer.Realize()
        main_sizer.Add(button_sizer, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

        # Bind enter key to find next
        self.find_textCtrl.Bind(wx.EVT_TEXT_ENTER, self.on_find_next)
        if self.mode == "replace":
            self.replace_textCtrl.Bind(wx.EVT_TEXT_ENTER, self.on_replace)

    def _update_search_flags(self) -> None:
        """Update search flags based on checkbox states."""
        self._search_flags = 0
        if self.match_case_checkbox.GetValue():
            self._search_flags |= wx.stc.STC_FIND_MATCHCASE
        if self.match_word_checkbox.GetValue():
            self._search_flags |= wx.stc.STC_FIND_WHOLEWORD

    def on_find_next(self, event: wx.CommandEvent) -> None:
        """Handle Find Next button click."""
        self._update_search_flags()
        find_text = self.find_textCtrl.GetValue()

        if not find_text:
            wx.MessageBox("Please enter text to find.", "Find", wx.OK | wx.ICON_INFORMATION, self)
            return

        # Store the search text for F3 (find next)
        self._last_search_text = find_text
        self.editor.SetSearchFlags(self._search_flags)
        self.editor.SetTargetStart(self.editor.GetSelectionEnd())
        self.editor.SetTargetEnd(self.editor.GetLength())

        pos = self.editor.SearchInTarget(find_text)

        if pos == -1:
            # Wrap around to beginning
            self.editor.SetTargetStart(0)
            self.editor.SetTargetEnd(self.editor.GetLength())
            pos = self.editor.SearchInTarget(find_text)

        if pos == -1:
            wx.MessageBox(f'"{find_text}" not found.', "Find", wx.OK | wx.ICON_INFORMATION, self)
        else:
            self.editor.GotoPos(pos)
            self.editor.SetSelectionStart(pos)
            self.editor.SetSelectionEnd(pos + len(find_text))

    def on_replace(self, event: wx.CommandEvent) -> None:
        """Handle Replace button click."""
        self._update_search_flags()
        find_text = self.find_textCtrl.GetValue()
        replace_text = self.replace_textCtrl.GetValue()

        if not find_text:
            wx.MessageBox("Please enter text to find.", "Replace", wx.OK | wx.ICON_INFORMATION, self)
            return

        # Check if there's a selection that matches
        if self.editor.GetSelectedText() == find_text:
            self.editor.ReplaceSelection(replace_text)

        # Find next occurrence
        self.on_find_next(event)

    def on_replace_all(self, event: wx.CommandEvent) -> None:
        """Handle Replace All button click."""
        self._update_search_flags()
        find_text = self.find_textCtrl.GetValue()
        replace_text = self.replace_textCtrl.GetValue()

        if not find_text:
            wx.MessageBox("Please enter text to find.", "Replace", wx.OK | wx.ICON_INFORMATION, self)
            return

        # Record start position for potential restore


        # Start from beginning
        self.editor.SetSearchFlags(self._search_flags)
        self.editor.SetTargetStart(0)
        self.editor.SetTargetEnd(self.editor.GetLength())

        replacements = 0

        while True:
            pos = self.editor.SearchInTarget(find_text)
            if pos == -1:
                break

            self.editor.SetTargetStart(pos)
            self.editor.SetTargetEnd(pos + len(find_text))
            self.editor.ReplaceTarget(replace_text)
            replacements += 1

            # Move past the replaced text
            self.editor.SetTargetStart(pos + len(replace_text))
            self.editor.SetTargetEnd(self.editor.GetLength())

        wx.MessageBox(f"Replaced {replacements} occurrence(s).", "Replace All", wx.OK | wx.ICON_INFORMATION, self)

    def on_close(self, event: wx.CommandEvent) -> None:
        """Handle Close button click."""
        self.Close()


def show_find_dialog(parent: wx.Window, editor: wx.stc.StyledTextCtrl) -> None:
    """Show the Find dialog."""
    FindReplaceDialog(parent, editor, mode="find")


def show_replace_dialog(parent: wx.Window, editor: wx.stc.StyledTextCtrl) -> None:
    """Show the Find and Replace dialog."""
    FindReplaceDialog(parent, editor, mode="replace")