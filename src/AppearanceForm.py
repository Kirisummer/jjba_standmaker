import tkinter as tk

from src.ColorEntry import ColorEntry
from src.NumberSlider import NumberSlider


class AppearanceForm(tk.LabelFrame):
    contour = None
    poly_fill = None
    poly_stroke = None

    def __init__(self, parent, translation):
        super().__init__(parent, text=translation['appearance_label'])
        self.contour = ColorEntry(self, translation['appearance_contour'], 'black')
        self.poly_fill = ColorEntry(self, translation['appearance_poly_fill'], 'magenta')
        self.poly_stroke = ColorEntry(self, translation['appearance_poly_stroke'], 'indigo')
        self.poly_opacity = NumberSlider(self, translation['appearance_poly_opacity'], 0.5, 0, 1, 0.01)
        self.contour.pack(fill='x', expand=True)
        self.poly_fill.pack(fill='x', expand=True)
        self.poly_stroke.pack(fill='x', expand=True)
        self.poly_opacity.pack(fill='x', expand=True)

    def translate(self, translation):
        self.config(text=translation['appearance_label'])
        self.contour.set_label(translation['appearance_contour'])
        self.poly_fill.set_label(translation['appearance_poly_fill'])
        self.poly_stroke.set_label(translation['appearance_poly_stroke'])
        self.poly_opacity.set_label(translation['appearance_poly_opacity'])
