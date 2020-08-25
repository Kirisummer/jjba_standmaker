import tkinter as tk


class NumberSlider(tk.Frame):
    valid = None

    def __init__(self, parent, label, default, min_value, max_value, step):
        super().__init__(parent)
        self.min_value = min_value
        self.max_value = max_value
        self.label = tk.Label(self, text=label)
        self.var = tk.StringVar()
        self.var.set(str(default))
        self.slider = tk.Scale(
                self,
                from_=min_value, to=max_value,
                resolution=step,
                orient=tk.HORIZONTAL,
                variable=self.var,
                showvalue=False
        )
        self.entry = tk.Entry(
                self,
                textvariable=self.var,
                width=4
        )
        self.var.trace('w', self.validate_entry)

        self.label.pack(side=tk.LEFT)
        self.entry.pack(side=tk.RIGHT)
        self.slider.pack(side=tk.RIGHT)

    def validate_entry(self, *args):
        self.entry.delete(4, tk.END)
        if not self.var.get():
            self.var.set('0')
        val = float(self.var.get())
        if self.min_value > val:
            self.var.set(str(self.min_value))
        elif self.max_value < val:
            self.var.set(str(self.max_value))

    def set_label(self, label):
        self.label.config(text=label)

    @property
    def value(self):
        return self.var.get()
