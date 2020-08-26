import tkinter as tk


class ColorEntry(tk.Frame):
    CANVAS_SIZE = 20
    entry_var = None
    
    def __init__(self, parent, label, default):
        super().__init__(parent)
        self.observers = []
        self.label = tk.Label(self, text=label)
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            self,
            textvariable=self.entry_var,
            width=10
        )
        self.canvas = tk.Canvas(
            self,
            width=self.CANVAS_SIZE,
            height=self.CANVAS_SIZE
        )
        self.entry_var.trace('w', self.update_canvas)
        self.entry_var.set(default)
        self.valid = None
        
        self.label.pack(side=tk.LEFT)
        self.canvas.pack(side=tk.RIGHT)
        self.entry.pack(side=tk.RIGHT)
    
    def update_canvas(self, *args):
        try:
            self.canvas.create_rectangle(
                0, 0,
                self.CANVAS_SIZE, self.CANVAS_SIZE,
                fill=self.entry_var.get()
            )
            self.entry.config(fg='black')
            self.valid = True
        except tk.TclError as e:
            self.valid = False
            if 'unknown color name' in str(e) or 'invalid color name' in str(e):
                self.entry.config(fg='red')
            else:
                raise e
        
        if not self.entry_var.get():
            self.valid = False
        self.notify_all()
    
    def set_label(self, label):
        self.label.config(text=label)
    
    @property
    def color(self):
        return self.entry.get()
    
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def notify_all(self):
        for observer in self.observers:
            observer.check_valid(self)
