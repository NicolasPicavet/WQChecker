# pylint: disable=anomalous-backslash-in-string

import threading
import datetime
import sys

import net.requester as requester
import gui.gui as gui
import utils
import config


regions = {'eu':'EU', 'na':'NA'}
region = config.region(lambda:'eu', False)
interval = config.interval(lambda:3 * utils.HOUR_IN_SECOND, False)
extensions = ['legion', 'bfa']
quests = config.getQuests()
# quests = {51974:None, 51976:None, 51977:None, 51978:None}

countdown = 0
    
def checkWQ():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    gui.mainView.setLastCheckValue(now)

    html = requester.getWorldQuestsHtml(extensions, region)

    try:
        for qid, qw in quests.items():
            if html.find('"url":"\/quest=' + str(qid) + '","') > 0:
                qw.setFound()
                gui.popupView(str(qid) + ' is up !')
            else:
                qw.setUnfound()
    except RuntimeError as e:
        # workaround when quests change size during loop
        print(e.__str__)
        checkWQ()
    print('Checked quests ' + str(quests.keys()) + ' at ' + now)
    
def changeRegion(newRegion):
    global region
    region = config.region(lambda:newRegion)
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
    gui.mainView.setNextCheckValue(countdown)
    countdown -= decrement
    timerCountdown = threading.Timer(decrement, countdownLoop)
    timerCountdown.start()

def exitApp():
    stopCountdown()
    stopTimer()
    sys.exit()

def registerQuest(questWidget=None, oldId=None):
    # there is an old id to remove
    if oldId != None:
        # remove from running data
        quests.pop(oldId)
        # remove from config data
        config.quest(oldId, None)
    # there is a new quest to add
    if questWidget != None:
        # check new quest id type
        try:
            qid = int(questWidget.id)
        except ValueError:
            print('Invalid value for quest id: "' + str(questWidget.id) + '"')
            questWidget.reset()
        # store in running data
        quests[qid] = questWidget
        # store in config data
        config.quest(qid, lambda:None)
        # fetch quest name
        def setQuestNameThread(questWidget):
            # if questWidget.id != '':
            questWidget.setQuestName(config.questCache(questWidget.id, lambda:requester.getQuestName(questWidget.id)))
            # else:
            #     questWidget.resetQuestName()
            #     questWidget.setUnchecked()
            return # close thread
        t = threading.Thread(target=setQuestNameThread, args=(questWidget,))
        t.setDaemon(True)
        t.start()

def setInterval(newInterval):
    global interval
    interval = config.interval(lambda:newInterval)
    checkerLoop()


mainView = gui.mainView.buildMainView(quests=quests, regions=regions, region=region, interval=interval, closeCallback=exitApp, regionCallback=changeRegion, checkNowCallback=checkWQ, questRegisterCallback=registerQuest, setIntervalCallback=setInterval)

checkerLoop()

mainView.mainloop()