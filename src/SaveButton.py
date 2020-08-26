import tkinter as tk


class SaveButton(tk.Button):
    def __init__(self, parent, **options):
        super().__init__(
                parent,
                command=lambda: parent.master.save_to_file(parent.entry_var.get()),
                **options
        )
        self.notifiers = dict()
    
    def check_valid(self, notifier):
        """
        if all of notifiers are valid then button activates
        :param notifier: must have valid field
        """
        self.notifiers[notifier] = notifier.valid
        
        if all(self.notifiers.values()):
            self['state'] = 'active'
        else:
            self['state'] = 'disabled'
