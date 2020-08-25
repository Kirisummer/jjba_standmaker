import tkinter as tk


class SaveButton(tk.Button):
    def __init__(self, parent, **options):
        super().__init__(
                parent,
                command=lambda: parent.master.save_to_file(parent.entry_var.get()),
                **options
        )
