# pylint: disable=anomalous-backslash-in-string

import net.requester as requester
import gui.gui as gui

import threading
import datetime

worldQuestsUrl = 'https://www.wowhead.com/world-quests/bfa/'
questUrl= 'https://www.wowhead.com/quest='
quests = {51974:None, 51976:None, 51977:None, 51978:None}
region = 'eu'
timerLength = 5
countdown = 0
    
def checkWQ():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    gui.mainView.setLastCheckValue(now)
    print('Check ' + str(quests.keys()) + ' at ' + now)

    html = requester.getWorldQuestsHtml(worldQuestsUrl + region)

    try:
        for qid, qw in quests.items():
            if str(html).find('"url":"\/quest=' + str(qid) + '","') > 0:
                qw.setFound()
                gui.popupView(str(qid) + ' is up !')
            else:
                qw.setUnfound()
    except RuntimeError as e:
        print(e.__str__)
        checkWQ()
    
def changeRegion(newRegion):
    global region
    region = newRegion
    checkerLoop()

def stopTimer():
    try:
        timer.cancel()
    except NameError:
        pass

def checkerLoop():
    global timer
    global countdown
    stopTimer()
    checkWQ()
    timer = threading.Timer(timerLength, checkerLoop)
    countdown = int(timerLength)
    countdownLoop()
    timer.start()

def stopCountdown():
    try:
        timerCountdown.cancel()
    except NameError:
        pass

def countdownLoop():
    global timerCountdown
    global countdown
    decrement = 1
    stopCountdown()
    gui.mainView.setNextCheckValue(countdown)
    countdown -= decrement
    timerCountdown = threading.Timer(decrement, countdownLoop)
    timerCountdown.start()

def exitApp():
    stopCountdown()
    stopTimer()
    exit()

def registerQuests():
    def setQuestNameThread(questWidget):
        if questWidget.id != '':
            questWidget.setQuestName(requester.getQuestName(questUrl + str(questWidget.id)))
        else:
            questWidget.resetQuestName()
            questWidget.setUnchecked()
    quests.clear()
    for qw in gui.mainView.questsWidgets:
        try:
            qid = int(qw.id)
        except ValueError:
            print('Invalid value for quest id: ' + str(qw.id))
            qw.reset()
        else:
            quests[qid] = qw
            threading.Thread(target=setQuestNameThread, args=(qw,)).start()

def unregisterQuest(questId):
    try:
        quests.pop(questId)
    except KeyError:
        print('Unregister quest ' + str(questId) + ' failed')
    else:
        print('Unregistered quest ' + str(questId))



statusView = gui.mainView.createStatusView(quests=quests, closeCallback=exitApp, regionCallback=changeRegion, checkNowCallback=checkWQ, questRegisterCallback=registerQuests, questUnregisterCallback=unregisterQuest)

checkerLoop()

statusView.mainloop()