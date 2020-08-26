import tkinter as tk

from LanguageButton import LanguageButton


class LanguageForm(tk.LabelFrame):
    buttons = {}

    def __init__(self, parent, translations, language):
        super().__init__(parent, text=translations[language]['lang_label'])
        for lang in translations:
            button = self.buttons[lang] = LanguageButton(self, lang, translations[lang]['lang_flag'])
            button.pack(side=tk.LEFT)

    def translate(self, translation):
        self.config(text=translation['lang_label'])
