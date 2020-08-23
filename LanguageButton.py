import tkinter as tk


class LanguageButton(tk.Button):
    lang = None
    flag = None

    def __init__(self, parent, lang, flag):
        self.flag = tk.PhotoImage(data=flag)
        super().__init__(
                parent,
                image=self.flag,
                width=24,
                height=18,
                command=lambda: parent.master.translate_app(lang)
        )
