from req import simple_get
import gui

from bs4 import BeautifulSoup

import threading
import datetime

url = 'https://www.wowhead.com/world-quests/bfa/'
quests = {51974:None, 51976:None, 51977:None, 51978:None}
region = 'eu'
timerLength = 5.0
    
def checkWQ():
    now = datetime.datetime.now()
    gui.setLastCheckValue(now.strftime("%Y-%m-%d %H:%M:%S"))
    gui.addStatusMsg(now.strftime("%Y-%m-%d %H:%M:%S"))

    # request
    raw_html = simple_get(url + region)

    # parse
    html = BeautifulSoup(raw_html, 'html.parser')

    # dump
    file = open('htmldump.html','w+')
    file.write(str(html))
    file.close()

    # scrap
    found = False
    for qid, qw in quests.items():
        if str(html).find('quest=' + str(qid)) > 0:
            qw.setFound()
            gui.addStatusMsg(str(qid) + ' is up !')
            gui.popupView(str(qid) + ' is up !')
            found = True
        else:
            qw.setUnfound()
    if not found:
        gui.addStatusMsg('No Sabertron are up :(')

    gui.addStatusMsg('')

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
    stopTimer()
    checkWQ()
    timer = threading.Timer(timerLength, checkerLoop)
    timer.start()

def exitApp():
    stopTimer()
    exit()

def registerQuests():
    quests.clear()
    for qw in gui.questsWidgets:
        quests[qw.questId] = qw



statusView = gui.createStatusView(quests=quests, closeCallback=exitApp, regionCallback=changeRegion, checkNowCallback=checkWQ, questRegisterCallback=registerQuests)

checkerLoop()

statusView.mainloop()