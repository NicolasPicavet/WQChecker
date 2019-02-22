import tkinter as tk
from PIL import ImageTk, Image

import gui.utils as utils


class questWidget:

    wqIconLabel = None
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

        questEntry = tk.Entry(self.widgetFrame, textvariable=questVar)
        questEntry.grid(row=0, column=0, sticky=tk.W)

        self.wqIconLabel = tk.Label(self.widgetFrame)
        self.wqIconLabel.grid(row=0, column=1)
        self.setUnchecked()

        self.questNameLabel = tk.Label(self.widgetFrame, text='...')
        self.questNameLabel.grid(row=0, column=2)

        deleteButton = tk.Button(self.widgetFrame, image=utils.deleteIcon, command=lambda:self.forgetWidgetThenCallback(deleteCallback))
        deleteButton.grid(row=0, column=3)

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
        self.wqIconLabel.config(image=icon)

    def setQuestName(self, questName):
        self.questNameLabel.config(text=questName)