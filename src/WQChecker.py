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
    now = datetime.datetime.now()
    gui.mainView.setLastCheckValue(now.strftime("%Y-%m-%d %H:%M:%S"))
    gui.mainView.addStatusMsg(now.strftime("%Y-%m-%d %H:%M:%S"))

    html = requester.getWorldQuestsHtml(worldQuestsUrl + region)

    for qid, qw in quests.items():
        if str(html).find('quest=' + str(qid)) > 0:
            qw.setFound()
            gui.popupView(str(qid) + ' is up !')
        else:
            qw.setUnfound()

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
        questWidget.setQuestName(requester.getQuestName(questUrl + str(questWidget.questId)))
        return
    quests.clear()
    for qw in gui.mainView.questsWidgets:
        quests[qw.questId] = qw
        threading.Thread(target=setQuestNameThread, args=(qw,)).start()



statusView = gui.mainView.createStatusView(quests=quests, closeCallback=exitApp, regionCallback=changeRegion, checkNowCallback=checkWQ, questRegisterCallback=registerQuests)

checkerLoop()

statusView.mainloop()