# WQChecker
Scrap WowHead data to monitor world quests status without manualy log into World of Warcraft and tediously check all regions and world quests.

## Run

Download the correct executable for your OS in [releases](https://github.com/NicolasPicavet/WQChecker/releases) and run it

#### from sources

You will need [python3](https://www.python.org/), [python**3**-pip](https://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3) and [python**3**-tk](https://stackoverflow.com/questions/6084416/tkinter-module-not-found-on-ubuntu)  
next
```
pip3 install beautifulsoup4 Pillow
```
then
```
python3 src/WQChecker.py
```

## Usage

![Screenshot version 4.1](https://i.imgur.com/uNKEACC.png "Screenshot version 4.1")

1. Select your Region
2. Add quest ids to track
3. A popup will warn you when a quest is up

#### How to find a quest id to track

1. Search for your quest on [WowHead](https://www.wowhead.com/) or [WowDB](https://www.wowdb.com/)
2. Look at your browser's address bar, e.g. https://www.wowhead.com/quest=52299
3. Copy the 5 digits number
4. Past it in WQChecker text input
5. Click on the green plus

