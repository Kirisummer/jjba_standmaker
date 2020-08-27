import tkinter as tk
from tkinter.filedialog import asksaveasfilename


class SaveButton(tk.Button):
    def __init__(self, parent, **options):
        super().__init__(
                parent,
                command=self.save_as,
                **options
        )
        self.notifiers = dict()
    
    def check_valid(self, notifier):
        """
        if all of notifiers are valid then button activates
        :param notifier: must have valid fiel
        """
        self.notifiers[notifier] = notifier.valid
        
        if all(self.notifiers.values()):
            self['state'] = 'active'
        else:
            self['state'] = 'disabled'

    def save_as(self):
        extensions = (('SVG image', '*.svg'), ('All files', '*.*'))
        filename = asksaveasfilename(
                master=self.master,
                filetypes=extensions,
                defaultextension=extensions
        )
        self.master.save_to_file(filename)
