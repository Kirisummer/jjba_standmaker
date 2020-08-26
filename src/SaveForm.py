import tkinter as tk

from src.BrowseButton import BrowseButton
from src.SaveButton import SaveButton


class SaveForm(tk.LabelFrame):
    entry_var = None
    entry = None
    browse_button = None
    save_button = None

    def __init__(self, parent, translation):
        super().__init__(parent, text=translation['save_label'])
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.browse_button = BrowseButton(self, text=translation['save_browse_button'])
        self.save_button = SaveButton(self, text=translation['save_save_button'])
        # Resize buttons
        max_width = max(len(translation['save_browse_button']), len(translation['save_save_button']))
        self.browse_button.config(width=max_width)
        self.save_button.config(width=max_width)
        # Align elements
        self.entry.pack(side=tk.LEFT, fill='x', expand=True)
        self.browse_button.pack()
        self.save_button.pack()

    def translate(self, translation):
        self.config(text=translation['save_label'])
        self.browse_button.config(text=translation['save_browse_button'])
        self.save_button.config(text=translation['save_save_button'])
        # Resize buttons
        max_width = max(len(translation['save_browse_button']), len(translation['save_save_button']))
        self.browse_button.config(width=max_width)
        self.save_button.config(width=max_width)
