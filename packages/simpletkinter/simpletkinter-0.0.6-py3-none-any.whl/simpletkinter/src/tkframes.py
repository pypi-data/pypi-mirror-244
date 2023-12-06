"""
Classes and methods to support tkinter GUI applications.
"""

import tkinter as tk
from tkinter import ttk
from collections import namedtuple

BORDER = 0
Coords = namedtuple("Coords", "row, col")


__all__ = ['Frame', 'ModalFrame']


class FrameBase():
    def __init__(self, parent):
        self.parent = parent
        self.row = 0

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
