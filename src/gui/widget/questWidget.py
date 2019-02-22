import tkinter as tk
from PIL import ImageTk, Image

from gui.utils import getAssetPath


class questWidget:

    wqIconLabel = None
    questId = None
    questStatusLabel = None
    widgetFrame = None
    questCallback = None

    def buildWidget(self, questsFrame, questCallback, questId):
        widgetFrame = tk.Frame(questsFrame)
        widgetFrame.pack(fill='both', expand=True)

        self.questId = questId
        questVar = tk.StringVar()
        questVar.set(questId)
        self.questCallback = questCallback
        questVar.trace('w', lambda name, index, mode, questVar=questVar: self.storeNewValueThenCallback(questVar.get()))

        questEntry = tk.Entry(widgetFrame, textvariable=questVar)
        questEntry.grid(row=0, column=0, sticky=tk.W)

        self.wqIconLabel = tk.Label(widgetFrame)
        self.wqIconLabel.grid(row=0, column=1)
        self.setUnchecked()

        self.questNameLabel = tk.Label(widgetFrame, text='...')
        self.questNameLabel.grid(row=0, column=2)

    def destroyWidget(self):
        self.widgetFrame.grid_forget()

    def storeNewValueThenCallback(self, newQuestId):
        self.questId = newQuestId
        self.questCallback()

    def setFound(self):
        self.updateStatus('found.png')

    def setUnchecked(self):
        self.updateStatus('unchecked.png')

    def setUnfound(self):
        self.updateStatus('unfound.png')

    def updateStatus(self, icon):
        statusIcon = ImageTk.PhotoImage(Image.open(getAssetPath(icon)))
        self.wqIconLabel.config(image=statusIcon)
        self.wqIconLabel.image = statusIcon # http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm

    def setQuestName(self, questName):
        self.questNameLabel.config(text=questName)