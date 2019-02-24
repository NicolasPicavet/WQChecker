import tkinter as tk

import utils
from gui.view.View import View


class FoundPopup(View):

    def buildFoundPopup(self, msg):
        self.root.wm_title('Is a Sabertron up ?')
        label = tk.Label(self.root, text=msg, font=('Helvetica', 10))
        label.pack(side='top', fill='x', pady=10)
        B1 = tk.Button(self.root, text='Okay', command = self.root.destroy)
        B1.pack()