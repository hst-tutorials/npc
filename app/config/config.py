from typing import Dict
from libs import speedtest
from libs import ping
import json

class Config:

    CONFIG = {
        "influxdb": {
            "name": "influxdb",
            "enabled": False,
            "host": "http:/localhost:8086",
            "token": "",
            "org": "",
        },
        "ookla": {
            "name": "ookla",
            "enabled": False,
            "bucket": "speedtest.net",
            "args": ["config", "name", ""],
            "module": speedtest.ookla
        },
        "iperf3": {
            "name": "iperf3",
            "enabled": True,
            "bucket": "iperf3",
            "hostname": "speedtest.group.asap.de",
            "port": "5202",
            "args": ["config", "hostname", "port"],
            "module": speedtest.iPerf3
        },
        "fastCom": {
            "name": "fastCom",
            "enabled": False,
            "bucket": "fast.com",
            "args": ["config","name",""],
            "module": speedtest.fastCom
        },
        "latency": {
            "name": "latency",
            "enabled": False,
            "hostnames": [
                "google.com", "fast.com"
            ],
            "count": 4,
            "bucket": "latency",
            "args": ["config", "hostnames", "count"],
            "module": ping.latency
        }
    }
    
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
        
        return config
                