from req import simple_get
import gui

from bs4 import BeautifulSoup

import threading
import datetime

url = 'https://www.wowhead.com/world-quests/bfa/'
quests = [51974, 51976, 51977, 51978]
region = 'eu'
timerLength = 5.0
    
def checkWQ():
    gui.addStatusMsg('=== Is a Sabertron up ? === in ' + region)
    now = datetime.datetime.now()
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
    for q in quests:
        if str(html).find(str(q)) > 0:
            gui.addStatusMsg(str(q) + ' is up !')
            gui.popupView(str(q) + ' is up !')
            found = True
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



statusView = gui.createStatusView(closeCallback=exitApp, regionCallback=changeRegion, checkNowCallback=checkWQ)

checkerLoop()

statusView.mainloop()