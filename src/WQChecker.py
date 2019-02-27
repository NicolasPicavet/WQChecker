# pylint: disable=anomalous-backslash-in-string

import threading
import datetime
import sys

import net.requester as requester
import utils
import config
import Constants

from gui.view.MainView import MainView
from gui.view.FoundPopup import FoundPopup


mainView = MainView()
foundPopups = {}

region = config.region(lambda:'eu', False)
interval = config.interval(lambda:3 * Constants.HOUR_IN_SECOND, False)
quests = config.getQuests()
# quests = {51974:None, 51976:None, 51977:None, 51978:None}

countdown = 0
    
def checkWQ():
    # there are quests needing checking
    if quests:
        now = datetime.datetime.now().strftime("%Y - %m - %d    %H : %M : %S")
        mainView.setLastCheckValue(now)
        
        html = requester.getWorldQuestsHtml(region)

        try:
            for qid, qw in quests.items():
                if html.find('"url":"\/quest=' + str(qid) + '","') > 0:
                    qw.setFound()
                    mainView.root.focus_force()

                    def createFoundPopup():
                        if not qid in foundPopups:
                            foundPopups[qid] = FoundPopup()
                            foundPopups[qid].buildFoundPopup(qid, qw.questName)
                            foundPopups[qid].mainLoop()
                    createFoundPopup()

                else:
                    qw.setUnfound()
        except RuntimeError as e:
            # workaround when quests change size during loop
            print(e.__str__)
            checkWQ()
        print('Checked quests ' + str(quests.keys()) + ' at ' + now)
    # no quest needs checking
    else:
        noQuestToCheck()

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
    timer = threading.Timer(interval, checkerLoop)
    countdown = interval
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
    mainView.setNextCheckValue(countdown)
    countdown -= decrement
    timerCountdown = threading.Timer(decrement, countdownLoop)
    timerCountdown.start()

def noQuestToCheck():
    stopTimer()
    stopCountdown()
    mainView.setNextCheckValue(-1)

def exitApp():
    stopCountdown()
    stopTimer()
    sys.exit()

def registerQuest(questWidget=None, oldId=None):
    # there is a quest subscription id to remove
    if oldId != None:
        # remove from running data
        quests.pop(oldId)
        # remove from config data
        config.quest(oldId, None)
        # that was the last quest
        if not quests:
            noQuestToCheck()
    # there is a new quest to add
    if questWidget != None:
        restart = False
        # first quest added, the loop will need to restart
        if not quests:
            restart = True
        # store in running data
        quests[questWidget.id] = questWidget
        # store in config data
        config.quest(questWidget.id, lambda:None)
        # restart after registering the first quest
        if restart:
            checkerLoop()
        # async quest name fetching
        def setQuestNameThread(questWidget):
            questWidget.setQuestName(config.questCache(questWidget.id, lambda:requester.getQuestName(questWidget.id)))
            return # close thread
        t = threading.Thread(target=setQuestNameThread, args=(questWidget,))
        t.setDaemon(True)
        t.start()

def setInterval(newInterval):
    global interval
    interval = config.interval(lambda:newInterval)
    checkerLoop()

def setRegion(newRegion):
    global region
    region = config.region(lambda:newRegion)
    checkerLoop()


mainView.buildMainView(quests=quests, region=region, interval=interval, closeCallback=exitApp, regionCallback=setRegion, checkNowCallback=checkWQ, questRegisterCallback=registerQuest, setIntervalCallback=setInterval)


# Keeping UI in main thread
def checkerLoopThread():
    if quests:
        checkerLoop()
    return # close thread
t = threading.Thread(target=checkerLoopThread)
t.setDaemon(True)
t.start()

mainView.mainLoop()