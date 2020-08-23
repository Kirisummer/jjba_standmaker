#TODO: add polygon opacity option

import enum
from math import cos, sin, radians

import json
import tkinter as tk
import tkinter.filedialog as fd
import lxml.etree as et


class ColorEntry(tk.Frame):
    CANVAS_SIZE = 20
    entry_var = None

    def __init__(self, parent, label, default):
        super().__init__(parent)
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

    def set_label(self, label):
        self.label.config(text=label)

    @property
    def color(self):
        return self.entry.get()


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

class Stat(enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'

    @staticmethod
    def values():
        return (Stat.A, Stat.B, Stat.C, Stat.D, Stat.E)

    def __int__(self):
        return 5 - ord(self.name) + ord('A')


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


class BrowseButton(tk.Button):
    def __init__(self, parent, **options):
        extensions = (('All files', '*.*'), ('SVG image', '*.svg'))
        super().__init__(
                parent,
                command=lambda: parent.entry_var.set(fd.asksaveasfilename(
                    filetypes=extensions, defaultextension=extensions
                )),
                **options
        )


class SaveButton(tk.Button):
    def __init__(self, parent, **options):
        super().__init__(
                parent,
                command=lambda: parent.master.save_to_file(parent.entry_var.get()),
                **options
        )


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


class LanguageForm(tk.LabelFrame):
    buttons = {}

    def __init__(self, parent, translations, language):
        super().__init__(parent, text=translations[language]['lang_label'])
        for lang in translations:
            button = self.buttons[lang] = LanguageButton(self, lang, translations[lang]['lang_flag'])
            button.pack(side=tk.LEFT)

    def translate(self, translation):
        self.config(text=translation['lang_label'])


class SaveForm(tk.LabelFrame):
    entry_var = None
    entry = None
    browse_button = None
    save_button = None

    def __init__(self, parent, translation):
        super().__init__(parent, text=translation['save_label'])
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.browse_button = BrowseButton(self, text=translation['save_browse_button'])
        self.save_button = SaveButton(self, text=translation['save_save_button'])
        # Resize buttons
        max_width = max(len(translation['save_browse_button']), len(translation['save_save_button']))
        self.browse_button.config(width=max_width)
        self.save_button.config(width=max_width)
        # Align elements
        self.entry.pack(side=tk.LEFT, fill='x', expand=True)
        self.browse_button.pack()
        self.save_button.pack()

    def translate(self, translation):
        self.config(text=translation['save_label'])
        self.browse_button.config(text=translation['save_browse_button'])
        self.save_button.config(text=translation['save_save_button'])
        # Resize buttons
        max_width = max(len(translation['save_browse_button']), len(translation['save_save_button']))
        self.browse_button.config(width=max_width)
        self.save_button.config(width=max_width)


class StandMaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)

        self.load_translations('translations.json')
        # default translation is the first one supplied (maybe?)
        language = next(iter(self.translations))
        translation = self.translations[language]

        self.title(translation['window_title'])

        self.appearance_form = AppearanceForm(self, translation)
        self.stats_form = StatsForm(self, translation)
        self.language_form = LanguageForm(self, self.translations, language)
        self.save_form = SaveForm(self, translation)

        self.stats_form.pack(side=tk.LEFT)
        self.language_form.pack(fill='both', expand=True)
        self.appearance_form.pack(fill='both', expand=True)
        self.save_form.pack(fill='both', expand=True)

    def load_translations(self, filename):
        with open(filename, encoding='utf-8') as f:
            self.translations = json.load(f)

    def translate_app(self, lang):
        translation = self.translations[lang]
        self.title(translation['window_title'])
        for form in ('appearance', 'stats', 'language', 'save'):
            getattr(self, f'{form}_form').translate(translation)

    def save_to_file(self, filename):
        # Calculate the points of the stat polygon
        CENTER = 64
        DISTANCE_BETWEEN_MARKS = 7
        stat_angles = {
                'power': radians(90),
                'speed': radians(30),
                'range': radians(330),
                'persistence': radians(270),
                'precision': radians(210),
                'development': radians(150)
        }
        stat_marks = {
                stat: getattr(self.stats_form, stat).value
                for stat in stat_angles
        }
        points = [
                (
                    CENTER + int(mark) * DISTANCE_BETWEEN_MARKS * cos(stat_angles[stat]),
                    CENTER - int(mark) * DISTANCE_BETWEEN_MARKS * sin(stat_angles[stat])
                )
                for stat, mark in stat_marks.items()
        ]

        # Import base.svg
        svg = et.parse('base.svg')

        # Draw polygon
        poly_group = svg.find('.//*[@id="polygon"]')
        poly = et.SubElement(
                poly_group,
                'polygon',
                attrib={
                    'points': ' '.join(map(lambda p: f'{p[0]},{p[1]}', points)),
                    'fill': self.appearance_form.poly_fill.color,
                    'stroke': self.appearance_form.poly_stroke.color,
                    'opacity': self.appearance_form.poly_opacity.value
                }
        )

        # Replace contour color
        svg.find('.//*[@id="line_color"]').getchildren()[0].attrib['stop-color'] = self.appearance_form.contour.color

        # Write svg
        svg.write(filename, pretty_print=True)


app = StandMaker()
app.mainloop()
