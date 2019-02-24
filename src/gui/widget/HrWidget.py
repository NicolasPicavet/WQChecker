import tkinter as tk

from gui.widget.Widget import Widget


class HrWidget(Widget):
    
    def __init__(self, parentFrame):
        tk.Frame(parentFrame, height=1, background='#BBB').pack(fill=tk.BOTH, expand=True, padx=10, pady=6)