import tkinter as tk

from Stat import Stat


class StatEntry(tk.Frame):
    option_var = None

    def __init__(self, parent, stat_name, value):
        super().__init__(parent)
        self.label = tk.Label(self, text=stat_name)
        self.option_var = tk.StringVar()
        self.option_var.set(value.name)
        self.options = tk.OptionMenu(
                self, self.option_var,
                *list(map(lambda v: v.name, Stat.values()))
        )
        self.label.pack(side=tk.LEFT)
        self.options.pack(side=tk.RIGHT)

    @property
    def value(self):
        return Stat(self.option_var.get())

    def set_stat_name(self, stat_name):
        self.label.config(text=stat_name)
