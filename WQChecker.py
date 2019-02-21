from req import simple_get
import gui

from bs4 import BeautifulSoup

import threading
import datetime

url = 'https://www.wowhead.com/world-quests/bfa/'
quests = [51974, 51976, 51977, 51978]
region = 'eu'
    
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

def stopChecker():
    timer.cancel()
    exit()

def checkerLoop():
    global timer
    checkWQ()
    timer = threading.Timer(5.0, checkerLoop)
    timer.start()



statusView = gui.createStatusView(stopChecker, region)

checkerLoop()

statusView.mainloop()