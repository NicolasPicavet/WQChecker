import tkinter as tk
from PIL import ImageTk, Image

import gui.utils as utils


class questWidget:

    questIconLabel = None
    id = None
    questStatusLabel = None
    widgetFrame = None

    questCallback = None

    def buildWidget(self, questsFrame, questCallback, deleteCallback, questId):
        self.questCallback = questCallback

        self.widgetFrame = tk.Frame(questsFrame)
        self.widgetFrame.pack(fill='both', expand=True)
        self.widgetFrame.grid_columnconfigure(2, weight=1)

        self.id = questId
        questVar = tk.StringVar()
        questVar.set(questId)
        questVar.trace('w', lambda name, index, mode, questVar=questVar: self.storeNewValueThenCallback(questVar.get()))

        questEntry = tk.Entry(self.widgetFrame, textvariable=questVar, width=utils.QUEST_ID_ENTRY_WIDTH)
        questEntry.grid(row=0, column=0, sticky=tk.W)

        self.questIconLabel = tk.Label(self.widgetFrame)
        self.questIconLabel.grid(row=0, column=1)

        self.questNameLabel = tk.Label(self.widgetFrame, anchor=tk.W)
        self.questNameLabel.grid(row=0, column=2, sticky=tk.W)

        deleteButton = tk.Button(self.widgetFrame, image=utils.deleteIcon, command=lambda:self.forgetWidgetThenCallback(deleteCallback))
        deleteButton.grid(row=0, column=3)
        
        self.reset()

    def forgetWidgetThenCallback(self, deleteCallback):
        self.widgetFrame.pack_forget()
        deleteCallback(self)

    def storeNewValueThenCallback(self, newQuestId):
        self.id = newQuestId
        self.questCallback()

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
