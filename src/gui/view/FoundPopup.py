import tkinter as tk

import AssetsLibrary as Assets
import utils
from gui.view.View import View


class FoundPopup(View):

    def buildFoundPopup(self, questId, questName):
        self.root.wm_title('World Quests Checker')
        self.root.tk.call('wm', 'iconphoto', self.root._w, Assets.favicon.data)
        self.root.resizable(False, False)
        self.root.minsize(200, 0)

        msg = questName + ' (' + str(questId) + ') found !'
        self.root.wm_title(msg)
        tk.Label(self.root, text=msg).pack(pady=10)
        tk.Button(self.root, text='Ok', command=self.root.destroy).pack()