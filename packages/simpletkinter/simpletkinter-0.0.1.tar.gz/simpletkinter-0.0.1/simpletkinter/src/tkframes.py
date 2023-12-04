"""
Classes and methods to support tkinter GUI applications.
"""

import tkinter as tk
from tkinter import ttk
from collections import namedtuple
from tkinter import StringVar
from tkwidgets import widgets

BORDER = 5
Coords = namedtuple("Coords", "row, col")


__all__ = ['Frame', 'ModalFrame']


class FrameBase():
    def __init__(self, parent):
        self.parent = parent
        self.row = 0

    def text_box(
        self,
        row: int,
        col: int,
        width: int,
        textvariable: StringVar,
        *args, **kwargs
    ) -> ttk.Entry:
        return widgets.text_box(
            self.frame,
            row,
            col,
            width,
            textvariable,
            *args,
            **kwargs
        )

    def combo_box(
        self,
        row: int,
        col: int,
        width: int,
        values: list,
        textvariable: StringVar,
        command: object = None,
        *args,
        **kwargs
    ) -> ttk.Combobox:
        return widgets.combo_box(
            self.frame,
            row,
            col,
            width,
            values,
            textvariable,
            command,
            *args,
            **kwargs
        )

    def radio_button(
        self,
        row: int,
        col: int,
        text: str,
        value: str,
        variable: StringVar,
        command: object = None,
        sticky=tk.W,
        *args,
        **kwargs
    ):
        return widgets.radio_button(
            self.frame,
            row,
            col,
            text,
            value,
            variable,
            sticky,
            command,
            *args,
            **kwargs
        )

    def quit_click(self, event) -> None:
        """Relay function on Cancel click."""
        quit()

    def quit(self):
        self.parent.root.destroy()


class Frame(FrameBase):
    def __init__(self, parent, container, row, col):
        super().__init__(parent)
        self.container = container
        self.frame = ttk.Frame(container)
        self.frame.grid(row=row, column=col, sticky=tk.W)

    def pad(self):
        # Pad widgets in frame
        # for widget in self.frame.winfo_children():
        #     widget.grid(padx=border, pady=border)
        ...


class ModalFrame(FrameBase):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title = title

        container = self.parent.root
        dlg = tk.Toplevel(container)
        self.dlg = dlg
        self.frame = dlg

        dlg.protocol("WM_DELETE_WINDOW", self.dismiss)
        dlg.transient(container)
        dlg.wait_visibility()
        dlg.grab_set()
        dlg.title(self.title)

        self.frame_widgets(dlg)

        dlg.wait_window()

    def dismiss(self):
        self.dlg.grab_release()
        self.dlg.destroy()

    def btn_dismiss(self, event):
        self.dismiss()
