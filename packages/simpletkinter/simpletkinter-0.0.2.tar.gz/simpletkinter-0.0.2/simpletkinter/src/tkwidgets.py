"""
Custom widget class to support tkinter GUI applications.

The widgets are created and displayed in a single call. They are named after the tkinter widgets.

The BaseWidget abstracts common elements. The *show* method handles placing the widgets on a grid.
"""

import tkinter as tk
from tkinter import ttk
from collections import namedtuple
from tkinter import StringVar

BORDER = 5
Coords = namedtuple("Coords", "row, col")


__all__ = ['Label', 'Entry', 'Spinbox', 'Button']


class BaseWidget():
    def __init__(self, frame, row: int, col: int, *args, **kwargs):
        self.row = row
        self.col = col
        self.border = BORDER
        self.container = frame.frame
        self.conf = {}
        kwargs_local = {
            'columnspan': 1,
            'sticky': tk.E,
            'padx':  self.border,
            'pady':  self.border,
            'command': None,
            'conf': {},
        }
        if 'conf' in kwargs:
            self.conf = kwargs['conf']
        self.kwargs = {key: item for key, item in kwargs.items() if key not in kwargs_local}
        self.display_params = self._get_display_params(kwargs_local, kwargs)
        self.widget = None

    def show(self):
        if not self.widget:
            return
        params = self.display_params
        self.widget.grid(
            row=self.row,
            column=self.col,
            columnspan=params.columnspan,
            sticky=params.sticky,
            padx=params.padx,
            pady=params.pady
        )

    @staticmethod
    def _get_display_params(kwargs_local, given_kwargs) -> dict:
        # Return the kwargs related to display from the given kwargs
        for key in kwargs_local:
            if key in given_kwargs:
                kwargs_local[key] = given_kwargs[key]
        return namedtuple('display_params', kwargs_local.keys())(*kwargs_local.values())


class Label(BaseWidget):
    def __init__(self, frame, row: int, col: int, *args, **kwargs):
        super().__init__(frame, row, col, *args, **kwargs)
        if args:
            self.kwargs['text'] = args[0]
        self.widget = ttk.Label(self.container, **self.kwargs)
        self.show()


class Entry(BaseWidget):
    def __init__(self, frame, row: int, col: int, *args, **kwargs):
        super().__init__(frame, row, col, *args, **kwargs)
        if args:
            self.kwargs['text'] = args[0]
        self.widget = tk.Entry(self.container, **self.kwargs)
        self.show()


class Spinbox(BaseWidget):
    def __init__(self, frame, row: int, col: int, *args, **kwargs):
        super().__init__(frame, row, col, *args, **kwargs)
        self.widget = ttk.Spinbox(self.container, **self.kwargs)
        self.show()


class Button(BaseWidget):
    def __init__(self, frame, row: int, col: int, *args, **kwargs):
        super().__init__(frame, row, col, *args, **kwargs)
        command = None
        if args:
            self.kwargs['text'] = args[0]
            if len(args) > 1:
                command = args[1]
        if 'command' in kwargs:
            command = kwargs['command']
        self.widget = ttk.Button(self.container, **self.kwargs)
        self.widget.bind("<Button-1>", command)
        self.show()


class Widgets():
    def __init__(self):
        self.border = BORDER

    def text_box(self,
                 frame,
                 row: int,
                 col: int,
                 width: int,
                 textvariable: StringVar,
                 *args,
                 **kwargs) -> ttk.Entry:
        kwargs_local = {
            'sticky': tk.E,
            'padx': BORDER,
            'pady': BORDER,
            'columnspan': 1,
        }
        kw = self._get_display_params(kwargs_local, kwargs)
        # Create and return text entry box
        text = ttk.Entry(frame, width=width, textvariable=textvariable)
        text.grid(row=row, column=col, sticky=kw.sticky, columnspan=kw.columnspan)
        return text

    def combo_box(
        self,
        frame,
        row: int,
        col: int,
        width: int,
        values: list,
        textvariable: StringVar,
        command: object = None,
        *args,
        **kwargs
    ) -> ttk.Combobox:
        # Create and return combo-box
        combo_box = ttk.Combobox(frame,
                                 width=width,
                                 values=values,
                                 textvariable=textvariable)
        combo_box.grid(row=row, column=col, sticky=tk.W)
        combo_box.bind('<<ComboboxSelected>>', command)
        return combo_box

    def radio_button(
        self,
        frame,
        row: int,
        col: int,
        text: str,
        value: str,
        variable: StringVar,
        sticky=tk.W,
        command: object = None,
        *args,
        **kwargs
    ) -> ttk.Radiobutton:
        # Create and return radio-button
        radio_button = ttk.Radiobutton(frame,
                                       text=text,
                                       value=value,
                                       variable=variable,
                                       command=command)
        radio_button.grid(row=row, column=col, sticky=sticky, *args, **kwargs)

    @staticmethod
    def _get_display_params(kwargs_local, kwargs_specific) -> dict:
        # Return the kwargs as a namedtuple after default is replaced by specific
        for key in kwargs_local:
            if key in kwargs_specific:
                kwargs_local[key] = kwargs_specific[key]
        kw = namedtuple('kw', kwargs_local.keys())(*kwargs_local.values())
        return kw


widgets = Widgets()
