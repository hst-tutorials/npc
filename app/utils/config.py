from posixpath import split
from pydoc import classname
from typing import Dict

import json
import sys

from utils import logging as log
from libs import bandwidth
from libs import ping


class Config:

    CONFIG_FILE = "/app/config/config.json"
    
    #open config file and load it into json
    with open(CONFIG_FILE, 'r') as CONFIG:
        CONFIG = json.load(CONFIG)

    #helper function to parse existing json into CONFIG variable
    def parseConfig(self):

        config: dict = dict()

        #loop through sections and transfer their values into the CONFIG
        for section in self.CONFIG:
            config.update({section: {}})
            args = []
            for key, val in self.CONFIG[section].items():
                #if the key is named "args" we need to parse the pseudo "variables" into their corresponding values: 
                # e.g. "hostname" will be parsed into the value of the "hostname key"
                if key == "args":
                    for arg in self.CONFIG[section][key]:
                        if arg == "config":
                            args.append(self.CONFIG)
                        elif arg != "":
                            args.append(self.CONFIG[section][arg])
                        else:
                            args.append("")
                    config[section].update({key: args})
                else:
                    config[section].update({key: val})
                #resolve module given in json to corrensponding python module and save it into key
                if key == "module":
                    splitVal = val.split('.')[0] + "." + val.split('.')[1]
                    module = sys.modules[splitVal]
                    function = val.split('.')[2]

                    config[section].update({key: getattr(module, function)})

        config = self.validateConfig(config)

        return config

    #helper function to check if the config is valid, if a key is missing from a feature, the whole feature gets disabled
    def validateConfig(self, config):

        for section in config:
            for key, val in config[section].items():
                if val == "":
                    log.writeLog(
                        f"Empty value '{key}'! Disabling feature '{config[section]['name']}'", "WARN", "stdout")
                    config[section]['enabled'] = False

        return config
