import time
import tkinter as tk
import webbrowser

import AssetsLibrary as Assets
import Constants

import net.requester as requester

from gui.view.View import View
from gui.widget.QuestWidget import QuestWidget
from gui.widget.HrWidget import HrWidget


class MainView(View):
    regionVar = None # prevent garbage collecting

    questsWidgets = []

    instructionFont = ('Helvetica', 10, 'bold')

    readmeGitHubUrl = 'https://github.com/NicolasPicavet/WQChecker#user-content-how-to-find-a-quest-id-to-track'

    def buildMainView(self, quests, region, interval, closeCallback, regionCallback, checkNowCallback, questRegisterCallback, setIntervalCallback):
        self.root.wm_title('World Quests Checker')
        self.root.tk.call('wm', 'iconphoto', self.root._w, Assets.favicon.data)
        self.root.resizable(False, False)
        self.root.minsize(400, 0)
        self.root.protocol("WM_DELETE_WINDOW", closeCallback)

        paddingFrame = tk.Frame(self.root, padx=7, pady=7, background=Constants.HR_BACKGROUND)
        paddingFrame.pack(fill=tk.BOTH, expand=True)

        mainFrame = tk.Frame(paddingFrame, padx=7, pady=7)
        mainFrame.pack(fill=tk.BOTH, expand=True)

        # Region

        regionFrame = tk.Frame(mainFrame)
        regionFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        regionFrame.grid_columnconfigure(0, weight=1)

        tk.Label(regionFrame, text='1. Select your region', anchor=tk.W, font=self.instructionFont).pack(fill=tk.BOTH, expand=True)
        
        self.regionVar = tk.StringVar(value=region)
        def _createRegionRadio(regionKey, regionName):
            tk.Radiobutton(regionFrame, text=regionName, variable=self.regionVar, value=regionKey, command=lambda:regionCallback(regionKey), tristatevalue=None).pack(side=tk.LEFT)
        for rkey, rname in Constants.REGIONS.items():
            _createRegionRadio(rkey, rname)

        # Horizontal separation
        HrWidget(mainFrame)

        # Quests help

        questsHelpFrame = tk.Frame(mainFrame)
        questsHelpFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        questsHelpFrame.grid_columnconfigure(0, weight=1)

        tk.Label(questsHelpFrame, text='2. Subscribe to quests using their ID number', anchor=tk.W, font=self.instructionFont).pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        tk.Button(questsHelpFrame, image=Assets.helpIcon.data, command=lambda:webbrowser.open_new(self.readmeGitHubUrl)).pack(side=tk.RIGHT, pady=2)

        # New quest subscription

        def newQuestSubscription(event=None):
            self.questsWidgets.append(buildQuestWidget(newQuestEntry.get()))
            newQuestEntry.delete(0, tk.END)

        newQuestFrame = tk.Frame(mainFrame)
        newQuestFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        newQuestFrame.grid_columnconfigure(1, weight=1)

        newQuestEntry = tk.Entry(newQuestFrame, width=Constants.QUEST_ID_ENTRY_WIDTH)
        newQuestEntry.grid(row=0, column=0, sticky=tk.W)
        newQuestEntry.bind('<Return>', newQuestSubscription)
        newQuestEntry.focus()

        tk.Button(newQuestFrame, image=Assets.addIcon.data, command=newQuestSubscription).grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

        # Quests subscriptions

        questsFrame = tk.Frame(mainFrame)
        questsFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        questsFrame.grid_columnconfigure(0, weight=1)

        def buildQuestWidget(q):
            qw = QuestWidget()
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
        
        # World Quests

        worldQuestsFrame = tk.Frame(mainFrame)
        worldQuestsFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        def _createExpansionButton(expansion, region):
            tk.Button(worldQuestsFrame, image=Assets.library[e].data, command=lambda:webbrowser.open_new(requester.getWorldQuestUrl(expansion, self.regionVar.get()))).pack(side=tk.RIGHT, padx=2)
        for e in Constants.EXPANSIONS:
            _createExpansionButton(e, region)

        # Horizontal separation
        HrWidget(mainFrame)

        # Interval

        intervalFrame = tk.Frame(mainFrame)
        intervalFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        intervalFrame.grid_columnconfigure(0, weight=1)

        tk.Label(intervalFrame, text='3. Set your check timer', anchor=tk.W, font=self.instructionFont).grid(row=0, column=0, sticky=tk.W + tk.N)

        tk.Label(intervalFrame, text='every', anchor=tk.W).grid(row=0, column=1, sticky=tk.N)

        intervalScale = tk.Scale(intervalFrame, from_=1, to=6, orient=tk.HORIZONTAL)
        intervalScale.set(round(interval / Constants.HOUR_IN_SECOND))
        intervalScale.config(command=lambda scaleValue:setIntervalCallback(int(scaleValue) * Constants.HOUR_IN_SECOND))
        intervalScale.grid(row=0, column=2)
        
        tk.Label(intervalFrame, text='hours', anchor=tk.W).grid(row=0, column=3, sticky=tk.N)

        # Next Check

        nextCheckFrame = tk.Frame(mainFrame)
        nextCheckFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        nextCheckFrame.grid_columnconfigure(0, weight=1)

        tk.Label(nextCheckFrame, text='Next check timer', anchor=tk.W).grid(row=1, column=0, sticky=tk.W)
        self.nextCheckLabel = tk.Label(nextCheckFrame, text='-- : -- : --', anchor=tk.W)
        self.nextCheckLabel.grid(row=1, column=1)

        # Last Check

        lastCheckFrame = tk.Frame(mainFrame)
        lastCheckFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        lastCheckFrame.grid_columnconfigure(0, weight=1)

        tk.Label(lastCheckFrame, text='Last check', anchor=tk.W).grid(row=1, column=0, sticky=tk.W)
        self.lastCheckLabel = tk.Label(lastCheckFrame, text='-- : -- : --', anchor=tk.W)
        self.lastCheckLabel.grid(row=1, column=1)

        # Horizontal separation
        HrWidget(mainFrame)

        # Buttons

        buttonsFrame = tk.Frame(mainFrame)
        buttonsFrame.pack(fill=tk.BOTH, expand=True, padx=2, pady=5)

        tk.Button(buttonsFrame, text='Check now', command=checkNowCallback).pack(padx=2, anchor=tk.E)

    def setLastCheckValue(self, value):
        self.lastCheckLabel.config(text=value)

    def setNextCheckValue(self, value):
        if value >= 24 * Constants.HOUR_IN_SECOND:
            value = '> 1 day'
        elif value < 0:
            value = '-- : -- : --'
        else:
            value = time.strftime('%H : %M : %S', time.gmtime(value))
        self.nextCheckLabel.config(text=value)
