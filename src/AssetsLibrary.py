from PIL import ImageTk, Image

import utils
import AssetsLibrary as Assets


class Asset:
    name = None
    loaded = False
    data = None

    def __init__(self, name):
        self.name = name
        Assets.library[self.name[:-4]] = self

    def load(self):
        if not self.loaded:
            self.loaded = True
            self.data = ImageTk.PhotoImage(Image.open(utils.getBundlePath('assets/' + self.name)))

def loadAssets():
    global library
    for a in library.values():
        a.load()


library = {}

favicon = Asset('favicon.png')
wowheadIcon = Asset('wowhead.png')
addIcon = Asset('add.png')
deleteIcon = Asset('delete.png')
foundIcon = Asset('found.png')
unfoundIcon = Asset('unfound.png')
uncheckedIcon = Asset('unchecked.png')
legionIcon = Asset('legion.png')
bfaIcon = Asset('bfa.png')
helpIcon = Asset('help.png')
