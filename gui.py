import tkinter as tk
from PIL import ImageTk, Image

import sys
import os
import time

# get tmp folder path generated by Pyinstaller bundle
def getBundlePath(file):
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, file)
    else:
        path = file
    return path

def popupView(msg):
    popupWindow = tk.Tk()
    popupWindow.wm_title('Is a Sabertron up ?')
    label = tk.Label(popupWindow, text=msg, font=('Helvetica', 10))
    label.pack(side='top', fill='x', pady=10)
    B1 = tk.Button(popupWindow, text='Okay', command = popupWindow.destroy)
    B1.pack()
    popupWindow.mainloop()

def createStatusView(quests, closeCallback, regionCallback, checkNowCallback, questRegisterCallback):
    global statusText
    global lastCheckLabel
    global nextCheckLabel
    global questsWidgets

    statusWindow = tk.Tk()
    statusWindow.wm_title('World Quests Checker')
    statusWindow.tk.call('wm', 'iconphoto', statusWindow._w, ImageTk.PhotoImage(Image.open(getBundlePath('icon.jpg'))))

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
    lastCheckLabel = tk.Label(lastCheckFrame, text='lastCheckValue', anchor=tk.W)
    lastCheckLabel.grid(row=1, column=1)

    # Next Check

    nextCheckFrame = tk.Frame(mainFrame)
    nextCheckFrame.grid(row=2, column=0, sticky='we', padx=2, pady=2)
    nextCheckFrame.grid_columnconfigure(0, weight=1)

    tk.Label(nextCheckFrame, text='Next check', anchor=tk.W).grid(row=1, column=0, sticky=tk.W)
    nextCheckLabel = tk.Label(nextCheckFrame, text='nextCheckValue', anchor=tk.W)
    nextCheckLabel.grid(row=1, column=1)

    # Quests subscriptions

    questsFrame = tk.Frame(mainFrame)
    questsFrame.grid(row=3, column=0, sticky='we', padx=2, pady=2)
    questsFrame.grid_columnconfigure(0, weight=1)

    def buildQuestWidget(q):
        qw = questWidget()
        qw.buildWidget(questsFrame=questsFrame, questCallback=questRegisterCallback, questId=q)
        return qw
    questsWidgets = []
    for qid in quests.keys():
        questsWidgets.append(buildQuestWidget(qid))
    questRegisterCallback()

    # New quest subscription

    newQuestFrame = tk.Frame(mainFrame)
    newQuestFrame.grid(row=4, column=0, sticky='we', padx=2, pady=2)
    newQuestFrame.grid_columnconfigure(0, weight=1)

    newQuestEntry = tk.Entry(newQuestFrame)
    newQuestEntry.grid(row=0, column=0, sticky='w')

    def newQuestSubscription():
        questsWidgets.append(buildQuestWidget(newQuestEntry.get()))
        questRegisterCallback()
        newQuestEntry.delete(0, tk.END)

    tk.Button(newQuestFrame, text='Subscribe', command=newQuestSubscription).grid(row=0, column=1, padx=2, pady=2)

    # Status text

    statusFrame = tk.Frame(mainFrame)
    statusFrame.grid(row=5, column=0, sticky='we', padx=2, pady=2)
    statusFrame.grid_columnconfigure(0, weight=1)

    statusText = tk.Text(statusFrame, font=('Helvetica', 10))
    statusText.grid(row=1, column=0, padx=2, pady=2)
    statusText.config(state=tk.DISABLED)

    statusTextScrollBar = tk.Scrollbar(statusFrame, command=statusText.yview)
    statusText['yscrollcommand'] = statusTextScrollBar.set
    statusTextScrollBar.grid(row=1, column=1, sticky='ns')

    # Buttons

    buttonsFrame = tk.Frame(mainFrame)
    buttonsFrame.grid(row=6, column=0, sticky='we', padx=2, pady=2)

    tk.Button(buttonsFrame, text='Check now', command=checkNowCallback).grid(row=0, column=0, padx=2, pady=2)
    tk.Button(buttonsFrame, text='Close', command=closeCallback).grid(row=0, column=1, padx=2, pady=2)

    return statusWindow

def setLastCheckValue(value):
    global lastCheckLabel
    lastCheckLabel.config(text=value)

def setNextCheckValue(value):
    global nextCheckLabel
    if value >= 60*60*24:
        value = '> 1 day'
    else:
        value = time.strftime('%H:%M:%S', time.gmtime(value))
    nextCheckLabel.config(text=value)

def addStatusMsg(msg):
    statusText.config(state=tk.NORMAL)
    statusText.insert(tk.END, msg + '\n')
    statusText.config(state=tk.DISABLED)


class questWidget:

    questStatusLabel = None
    status = None
    questId = None
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

        self.questStatusLabel = tk.Label(widgetFrame, text=self.status)
        self.questStatusLabel.grid(row=0, column=1)

        self.setUnchecked()

    def destroyWidget(self):
        self.widgetFrame.grid_forget()

    def storeNewValueThenCallback(self, newQuestId):
        self.questId = newQuestId
        self.questCallback()

    def setFound(self):
        self.status = 'F'
        self.updateStatus()

    def setUnchecked(self):
        self.status = '?'
        self.updateStatus()

    def setUnfound(self):
        self.status = 'N'
        self.updateStatus()

    def updateStatus(self):
        self.questStatusLabel.config(text=self.status)
