import configparser
import os
from opcode import hasname

import utils

CONFIG_FILE_NAME = './WQChecker.conf'

SETTINGS_SECTION = 'settings'

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

def _getConfig(section, key, defaultValue):
    if config.has_section(section):
        if config.has_option(section, key):
            if defaultValue != None:
                if type(defaultValue) == int:
                    return config.getint(section, key)
            return config.get(section, key)
        elif defaultValue != None:
            _writeConfig(lambda:_setConfig(section, key, defaultValue))
            return _getConfig(section, key, defaultValue)
        else:
            raise ValueError('Config key missing and no default value given')
    else:
        _writeConfig(lambda:config.add_section(section))
        return _getConfig(section, key, defaultValue)

def _getSetConfig(section, key, newValue, defaultValue=None):
    return _getConfig(section, key, defaultValue) if newValue == None else _setConfig(section, key, newValue)


def region(newValue=None):
    return _getSetConfig(SETTINGS_SECTION, REGION_KEY, newValue, 'eu')

def interval(newValue=None):
    return _getSetConfig(SETTINGS_SECTION, INTERVAL_KEY, newValue, 3 * utils.HOUR_IN_SECOND)


config = configparser.ConfigParser()
config.read(CONFIG_FILE_NAME)
