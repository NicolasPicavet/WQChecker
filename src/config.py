import configparser
import os
from opcode import hasname

import utils

CONFIG_FILE_NAME = './WQChecker.conf'

SETTINGS_SECTION = 'settings'
QUEST_CACHE_SECTION = 'quest cache'

INTERVAL_KEY = 'interval'
REGION_KEY = 'region'


def _setConfig(section, key, value):
    _writeConfig(lambda:config.set(str(section), str(key), str(value)))
    return value

def _writeConfig(writeAction):
    configFile = open(CONFIG_FILE_NAME,'w')
    writeAction()
    config.write(configFile)
    configFile.close()
    config.read(CONFIG_FILE_NAME)

def _getConfig(section, key, setCallback, overwrite, returnType=str):
    # ensure string for key and section
    section = str(section)
    key = str(key)
    # section already exist
    if config.has_section(section):
        # option already exist
        if config.has_option(section, key):
            # this config call is a setter
            if setCallback != None and overwrite:
                _writeConfig(lambda:config.remove_option(section, key))
                return _getConfig(section, key, setCallback, overwrite, returnType)
            # return value with correct type
            if returnType == int:
                return config.getint(section, key)
            return config.get(section, key)
        # add option with value from setCallback
        else:
            return _setConfig(section, key, setCallback())
    # add section if unexisting
    else:
        _writeConfig(lambda:config.add_section(section))
        return _getConfig(section, key, setCallback, overwrite, returnType)


def region(setCallback=None, overwrite=True):
    return _getConfig(SETTINGS_SECTION, REGION_KEY, setCallback, overwrite)

def interval(setCallback=None, overwrite=True):
    return _getConfig(SETTINGS_SECTION, INTERVAL_KEY, setCallback, overwrite, int)

def questCache(questKey, setCallback=None):
    return _getConfig(QUEST_CACHE_SECTION, questKey, setCallback, False)


config = configparser.ConfigParser()
config.read(CONFIG_FILE_NAME)
