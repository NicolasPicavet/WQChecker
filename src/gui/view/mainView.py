import time
import tkinter as tk

import utils
from gui.widget.questWidget import questWidget

def hr(parentFrame):
    tk.Frame(parentFrame, height=1, background='#BBB').pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

class mainView:

    root = tk.Tk()

    statusText = None
    lastCheckLabel = None
    nextCheckLabel = None
    questsWidgets = []

    def __init__(self):
        utils.loadAssets()

    def buildMainView(self, quests, regions, region, interval, closeCallback, regionCallback, checkNowCallback, questRegisterCallback, setIntervalCallback):

        self.root.wm_title('World Quests Checker')
        self.root.tk.call('wm', 'iconphoto', self.root._w, utils.favicon)
        self.root.resizable(False, False)
        self.root.minsize(300, 0)
        self.root.protocol("WM_DELETE_WINDOW", closeCallback)

        mainFrame = tk.Frame(self.root)
        mainFrame.pack(fill=tk.BOTH, expand=True)

        # Region

        regionFrame = tk.Frame(mainFrame)
        regionFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        regionFrame.grid_columnconfigure(0, weight=1)

        tk.Label(regionFrame, text='Region', anchor=tk.W).pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        regionVar = tk.IntVar()
        def createRegionRadio(regionKey, regionName):
            return tk.Radiobutton(regionFrame, text=regionName, variable=regionVar, value=regionKey, command=lambda:regionCallback(regionKey))
        for rkey, rname in regions.items():
            radioButton = createRegionRadio(rkey, rname)
            radioButton.pack(side=tk.LEFT)
            if rkey == region:
                radioButton.select()

        # Horizontal separation
        hr(mainFrame)

        # Last Check

        lastCheckFrame = tk.Frame(mainFrame)
        lastCheckFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        lastCheckFrame.grid_columnconfigure(0, weight=1)

        tk.Label(lastCheckFrame, text='Last check', anchor=tk.W).grid(row=1, column=0, sticky=tk.W)
        self.lastCheckLabel = tk.Label(lastCheckFrame, text='lastCheckValue', anchor=tk.W)
        self.lastCheckLabel.grid(row=1, column=1)

        # Next Check

        nextCheckFrame = tk.Frame(mainFrame)
        nextCheckFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        nextCheckFrame.grid_columnconfigure(0, weight=1)

        tk.Label(nextCheckFrame, text='Next check', anchor=tk.W).grid(row=1, column=0, sticky=tk.W)
        self.nextCheckLabel = tk.Label(nextCheckFrame, text='nextCheckValue', anchor=tk.W)
        self.nextCheckLabel.grid(row=1, column=1)

        # Interval

        intervalFrame = tk.Frame(mainFrame)
        intervalFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        intervalFrame.grid_columnconfigure(0, weight=1)

        tk.Label(intervalFrame, text='Interval', anchor=tk.W).grid(row=0, column=0, sticky=tk.W + tk.N)

        intervalScale = tk.Scale(intervalFrame, from_=1, to=6, orient=tk.HORIZONTAL)
        intervalScale.set(round(interval / utils.HOUR_IN_SECOND))
        intervalScale.config(command=lambda scaleValue:setIntervalCallback(int(scaleValue) * utils.HOUR_IN_SECOND))
        intervalScale.grid(row=0, column=1)
        
        tk.Label(intervalFrame, text='hours', anchor=tk.W).grid(row=0, column=2, sticky=tk.N)

        # Horizontal separation
        hr(mainFrame)

        # Quests subscriptions

        questsFrame = tk.Frame(mainFrame)
        questsFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        questsFrame.grid_columnconfigure(0, weight=1)

        def buildQuestWidget(q):
            qw = questWidget()

            def removeQuestWidgetThenCallback(questWidget):
                try:
                    self.questsWidgets.remove(questWidget)
                    questRegisterCallback(oldId=questWidget.id)
                except ValueError:
                    print('Remove questWidget ' + str(questWidget) + ' failed')

            qw.buildWidget(questsFrame=questsFrame, registerCallback=questRegisterCallback, deleteCallback=removeQuestWidgetThenCallback, questId=q)
            return qw
            
        self.questsWidgets = []
        for qid in quests.keys():
            self.questsWidgets.append(buildQuestWidget(qid))

        # New quest subscription

        def newQuestSubscription(event=None):
            self.questsWidgets.append(buildQuestWidget(newQuestEntry.get()))
            newQuestEntry.delete(0, tk.END)

        newQuestFrame = tk.Frame(mainFrame)
        newQuestFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        newQuestFrame.grid_columnconfigure(1, weight=1)

        newQuestEntry = tk.Entry(newQuestFrame, width=utils.QUEST_ID_ENTRY_WIDTH)
        newQuestEntry.grid(row=0, column=0, sticky=tk.W)
        newQuestEntry.bind('<Return>', newQuestSubscription)

        tk.Button(newQuestFrame, image=utils.addIcon, command=newQuestSubscription).grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

        # Horizontal separation
        hr(mainFrame)

        # Buttons

        buttonsFrame = tk.Frame(mainFrame)
        buttonsFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=5)

        tk.Button(buttonsFrame, text='Check now', command=checkNowCallback).pack(padx=2, anchor=tk.E)

        return self.root

    def setLastCheckValue(self, value):
        self.lastCheckLabel.config(text=value)

    def setNextCheckValue(self, value):
        if value >= 24 * utils.HOUR_IN_SECOND:
            value = '> 1 day'
        else:
            value = time.strftime('%H:%M:%S', time.gmtime(value))
        self.nextCheckLabel.config(text=value)
