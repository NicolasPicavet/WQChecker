import tkinter as tk

import AssetsLibrary


class View:
    root = tk.Tk()

    def __init__(self):
        AssetsLibrary.loadAssets()

    def mainLoop(self):
        self.root.mainloop()
        