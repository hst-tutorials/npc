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

    with open(CONFIG_FILE, 'r') as CONFIG:
        CONFIG = json.load(CONFIG)

    def parseConfig(self):

        config: dict = dict()

        for section in self.CONFIG:
            config.update({section: {}})
            args = []
            for key, val in self.CONFIG[section].items():
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
                if key == "module":
                    splitVal = val.split('.')[0] + "." + val.split('.')[1]
                    module = sys.modules[splitVal]
                    function = val.split('.')[2]

                    config[section].update({key: getattr(module, function)})

        config = self.validateConfig(config)

        return config

    def validateConfig(self, config):

        for section in config:
            for key, val in config[section].items():
                if val == "":
                    log.writeLog(
                        f"Empty value '{key}'! Disabling feature '{config[section]['name']}'", "WARN", "stdout")
                    config[section]['enabled'] = False

        return config
