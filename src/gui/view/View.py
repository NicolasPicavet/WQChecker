import tkinter as tk

import AssetsLibrary


MASTER = tk.Tk()
MASTER.withdraw()

class View:
    def __init__(self):
        self.root = tk.Toplevel()
        AssetsLibrary.loadAssets()

    def mainLoop(self):
        self.root.mainloop()
        