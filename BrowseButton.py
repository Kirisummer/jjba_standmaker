import tkinter as tk
from tkinter import filedialog


class BrowseButton(tk.Button):
    def __init__(self, parent, **options):
        extensions = (('SVG image', '*.svg'), ('All files', '*.*'))
        super().__init__(
                parent,
                command=lambda: parent.entry_var.set(filedialog.asksaveasfilename(
                    filetypes=extensions, defaultextension=extensions
                )),
                **options
        )
