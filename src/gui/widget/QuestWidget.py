import tkinter as tk
from PIL import ImageTk, Image
import webbrowser

import utils
import AssetsLibrary as Assets
import net.requester as requester
import Constants

from gui.widget.Widget import Widget


class QuestWidget(Widget):

    def _getQuestId(self):
        return self.__QuestId
    def _setQuestId(self, value):
        try:
            self.__QuestId = int(value)
        except ValueError:
            raise TypeError("QuestId must be an integer")
    id = property(_getQuestId, _setQuestId)

    def buildWidget(self, questsFrame, registerCallback, deleteCallback, questId):
        self.registerCallback = registerCallback
        self.id = questId

        self.widgetFrame = tk.Frame(questsFrame)
        self.widgetFrame.pack(fill='both', expand=True)
        self.widgetFrame.grid_columnconfigure(2, weight=1)

        questVar = tk.StringVar()
        questVar.set(questId)
        questVar.trace('w', lambda name, index, mode, questVar=questVar: self.storeNewValueThenCallback(questVar.get()))

        questEntry = tk.Entry(self.widgetFrame, textvariable=questVar, width=Constants.QUEST_ID_ENTRY_WIDTH)
        questEntry.grid(row=0, column=0, sticky=tk.W)

        self.questIconLabel = tk.Label(self.widgetFrame)
        self.questIconLabel.grid(row=0, column=1)

        self.questNameLabel = tk.Label(self.widgetFrame, anchor=tk.W)
        self.questNameLabel.grid(row=0, column=2, sticky=tk.W)

        tk.Button(self.widgetFrame, image=Assets.wowheadIcon.data, command=lambda:webbrowser.open_new(requester.getQuestUrl(self.id))).grid(row=0, column=3, padx=2)

        tk.Button(self.widgetFrame, image=Assets.deleteIcon.data, command=lambda:self.forgetWidgetThenCallback(deleteCallback)).grid(row=0, column=4, padx=2)
        
        self.reset()
        self.registerCallback(self)

    def forgetWidgetThenCallback(self, deleteCallback):
        self.widgetFrame.pack_forget()
        deleteCallback(self)

    def storeNewValueThenCallback(self, newId):
        oldId = self.id
        self.id = newId
        self.registerCallback(self, oldId)

    def setFound(self):
        self.updateStatus(Assets.foundIcon.data)

    def setUnchecked(self):
        self.updateStatus(Assets.uncheckedIcon.data)

    def setUnfound(self):
        self.updateStatus(Assets.unfoundIcon.data)

    def updateStatus(self, icon):
        self.questIconLabel.config(image=icon)

    def setQuestName(self, questName):
        self.questName = questName
        self.questNameLabel.config(text=questName)

    def reset(self):
        self.setQuestName('...')
        self.setUnchecked()
