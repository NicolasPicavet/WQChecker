import time
import tkinter as tk
from PIL import ImageTk, Image

from gui.utils import getAssetPath
from gui.widget.questWidget import questWidget

class mainView:

    statusText = None
    lastCheckLabel = None
    nextCheckLabel = None
    questsWidgets = []

    def createStatusView(self, quests, closeCallback, regionCallback, checkNowCallback, questRegisterCallback):
        statusWindow = tk.Tk()
        statusWindow.wm_title('World Quests Checker')
        statusWindow.tk.call('wm', 'iconphoto', statusWindow._w, ImageTk.PhotoImage(Image.open(getAssetPath('icon.jpg'))))

        mainFrame = tk.Frame(statusWindow)
        mainFrame.pack(fill='both', expand=True)

        # Radio buttons

        radioFrame = tk.Frame(mainFrame)
        radioFrame.grid(row=0, column=0, sticky='we', padx=2, pady=2)
        radioFrame.grid_columnconfigure(0, weight=1)

        tk.Label(radioFrame, text='Region', anchor=tk.W).grid(row=0, column=0, sticky=tk.W)

        region = None
        naRadio = tk.Radiobutton(radioFrame, text='NA', variable=region, value='na', command=lambda:regionCallback('na'))
        naRadio.grid(row=0, column=2)
        euRadio = tk.Radiobutton(radioFrame, text='EU', variable=region, value='eu', command=lambda:regionCallback('eu'))
        euRadio.grid(row=0, column=1)
        euRadio.select()

        # Last Check

        lastCheckFrame = tk.Frame(mainFrame)
        lastCheckFrame.grid(row=1, column=0, sticky='we', padx=2, pady=2)
        lastCheckFrame.grid_columnconfigure(0, weight=1)

        tk.Label(lastCheckFrame, text='Last check', anchor=tk.W).grid(row=1, column=0, sticky=tk.W)
        self.lastCheckLabel = tk.Label(lastCheckFrame, text='lastCheckValue', anchor=tk.W)
        self.lastCheckLabel.grid(row=1, column=1)

        # Next Check

        nextCheckFrame = tk.Frame(mainFrame)
        nextCheckFrame.grid(row=2, column=0, sticky='we', padx=2, pady=2)
        nextCheckFrame.grid_columnconfigure(0, weight=1)

        tk.Label(nextCheckFrame, text='Next check', anchor=tk.W).grid(row=1, column=0, sticky=tk.W)
        self.nextCheckLabel = tk.Label(nextCheckFrame, text='nextCheckValue', anchor=tk.W)
        self.nextCheckLabel.grid(row=1, column=1)

        # Quests subscriptions

        questsFrame = tk.Frame(mainFrame)
        questsFrame.grid(row=3, column=0, sticky='we', padx=2, pady=2)
        questsFrame.grid_columnconfigure(0, weight=1)

        def buildQuestWidget(q):
            qw = questWidget()
            qw.buildWidget(questsFrame=questsFrame, questCallback=questRegisterCallback, questId=q)
            return qw
        self.questsWidgets = []
        for qid in quests.keys():
            self.questsWidgets.append(buildQuestWidget(qid))
        questRegisterCallback()

        # New quest subscription

        newQuestFrame = tk.Frame(mainFrame)
        newQuestFrame.grid(row=4, column=0, sticky='we', padx=2, pady=2)
        newQuestFrame.grid_columnconfigure(0, weight=1)

        newQuestEntry = tk.Entry(newQuestFrame)
        newQuestEntry.grid(row=0, column=0, sticky='w')

        def newQuestSubscription():
            self.questsWidgets.append(buildQuestWidget(newQuestEntry.get()))
            questRegisterCallback()
            newQuestEntry.delete(0, tk.END)

        tk.Button(newQuestFrame, text='Subscribe', command=newQuestSubscription).grid(row=0, column=1, padx=2, pady=2)

        # Status text

        statusFrame = tk.Frame(mainFrame)
        statusFrame.grid(row=5, column=0, sticky='we', padx=2, pady=2)
        statusFrame.grid_columnconfigure(0, weight=1)

        self.statusText = tk.Text(statusFrame, font=('Helvetica', 10))
        self.statusText.grid(row=1, column=0, padx=2, pady=2)
        self.statusText.config(state=tk.DISABLED)

        statusTextScrollBar = tk.Scrollbar(statusFrame, command=self.statusText.yview)
        self.statusText['yscrollcommand'] = statusTextScrollBar.set
        statusTextScrollBar.grid(row=1, column=1, sticky='ns')

        # Buttons

        buttonsFrame = tk.Frame(mainFrame)
        buttonsFrame.grid(row=6, column=0, sticky='we', padx=2, pady=2)

        tk.Button(buttonsFrame, text='Check now', command=checkNowCallback).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(buttonsFrame, text='Close', command=closeCallback).grid(row=0, column=1, padx=2, pady=2)

        return statusWindow

    def setLastCheckValue(self, value):
        self.lastCheckLabel.config(text=value)

    def setNextCheckValue(self, value):
        if value >= 60*60*24:
            value = '> 1 day'
        else:
            value = time.strftime('%H:%M:%S', time.gmtime(value))
        self.nextCheckLabel.config(text=value)

    def addStatusMsg(self, msg):
        self.statusText.config(state=tk.NORMAL)
        self.statusText.insert(tk.END, msg + '\n')
        self.statusText.config(state=tk.DISABLED)