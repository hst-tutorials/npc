
import configparser
import json


def getCorrectFallback(section):
    return "False" if section == "features" else ""


def getConfig(configType):

    if configType == "configFile":
        configFile = "/app/config/config.ini"

        config = configparser.ConfigParser()
        config.read(configFile)

        configDict: dict = dict()

        for section in config.sections():
            configDict.update({section: {}})
            for (key, val) in config.items(section):
                configDict[section].update(
                    {key: config.get(section, key, fallback=getCorrectFallback(section))})

        print(configDict)

        return config
