import tkinter as tk
from PIL import ImageTk, Image
import webbrowser

import utils
import net.requester as requester


class questWidget:

    questIconLabel = None
    id = None
    questStatusLabel = None
    widgetFrame = None

    registerCallback = None

    def buildWidget(self, questsFrame, registerCallback, deleteCallback, questId):
        self.registerCallback = registerCallback
        self.id = questId

        self.widgetFrame = tk.Frame(questsFrame)
        self.widgetFrame.pack(fill='both', expand=True)
        self.widgetFrame.grid_columnconfigure(2, weight=1)

        questVar = tk.StringVar()
        questVar.set(questId)
        questVar.trace('w', lambda name, index, mode, questVar=questVar: self.storeNewValueThenCallback(questVar.get()))

        questEntry = tk.Entry(self.widgetFrame, textvariable=questVar, width=utils.QUEST_ID_ENTRY_WIDTH)
        questEntry.grid(row=0, column=0, sticky=tk.W)

        self.questIconLabel = tk.Label(self.widgetFrame)
        self.questIconLabel.grid(row=0, column=1)

        self.questNameLabel = tk.Label(self.widgetFrame, anchor=tk.W)
        self.questNameLabel.grid(row=0, column=2, sticky=tk.W)

        tk.Button(self.widgetFrame, image=utils.wowheadIcon, command=self._webLinkCallback).grid(row=0, column=3, padx=2)

        tk.Button(self.widgetFrame, image=utils.deleteIcon, command=lambda:self.forgetWidgetThenCallback(deleteCallback)).grid(row=0, column=4, padx=2)
        
        self.registerCallback(self)
        self.reset()

    def _webLinkCallback(self):
        webbrowser.open_new(requester.getQuestUrl(self.id))

    def forgetWidgetThenCallback(self, deleteCallback):
        self.widgetFrame.pack_forget()
        deleteCallback(self)

    def storeNewValueThenCallback(self, newId):
        oldId = self.id
        self.id = newId
        self.registerCallback(self, oldId)

    def setFound(self):
        self.updateStatus(utils.foundIcon)

    def setUnchecked(self):
        self.updateStatus(utils.uncheckedIcon)

    def setUnfound(self):
        self.updateStatus(utils.unfoundIcon)

    def updateStatus(self, icon):
        self.questIconLabel.config(image=icon)

    def setQuestName(self, questName):
        self.questNameLabel.config(text=questName)

    def reset(self):
        self.setQuestName('...')
        self.setUnchecked()
