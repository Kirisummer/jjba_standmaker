import tkinter as tk

from src.Stat import Stat
from src.StatEntry import StatEntry


class StatsForm(tk.LabelFrame):
    power = None
    speed = None
    range = None
    persistence = None
    precision = None
    development = None

    def __init__(self, parent, translation):
        super().__init__(parent, text=translation['stat_label'])
        stats = {
            'power': Stat.A,
            'speed': Stat.A,
            'range': Stat.D,
            'persistence': Stat.B,
            'precision': Stat.B,
            'development': Stat.C
        }
        for i, (stat, value) in enumerate(stats.items()):
            setattr(self, stat, StatEntry(self, translation[f'stat_{stat}'], value))
            getattr(self, stat).pack(fill='x', expand=True)

    def translate(self, translation):
        self.config(text=translation['stat_label'])
        for stat in ('power', 'speed', 'range', 'persistence', 'precision', 'development'):
            getattr(self, stat).set_stat_name(translation[f'stat_{stat}'])
