
import os,configparser
import json

def getConfig(configType):
    
    if configType == "configFile":
        configFile ="/app/config/config.ini"
        
        config = configparser.ConfigParser()
        config.read(configFile)
        
        config = {
            "features": {
                "OoklaSpeedtestEnabled": config.get('features','OoklaSpeedtestEnabled') if config.has_option('features','OoklaSpeedtestEnabled') else "False",
                "iPerf3SpeedtestEnabled": config.get('features','iPerf3SpeedtestEnabled') if config.has_option('features','iPerf3SpeedtestEnabled') else "False",
                "latencyCheckEnabled": config.get('features','latencyCheckEnabled') if config.has_option('features','latencyCheckEnabled') else "False",
                "influxDBEnabled": config.get('features','influxDBEnabled') if config.has_option('features','influxDBEnabled') else "False",
            },
            "settings": {
                "ooklaBucket": config.get('settings','ooklaBucket') if config.has_option('settings','ooklaBucket') else "npc",
                "iPerf3Hostname": config.get('settings','iPerf3Hostname') if config.has_option('settings','iPerf3Hostname') else "",
                "iPerf3Port": config.get('settings','iPerf3Port') if config.has_option('settings','iPerf3Port') else "",
                "iPerf3Bucket": config.get('settings','iPerf3Bucket') if config.has_option('settings','iPerf3Bucket') else "npc",
                "latencyCheckHostnames": json.loads(config.get('settings','latencyCheckHostnames')) if config.has_option('settings','latencyCheckHostnames') else "",
                "latencyCheckCount": config.get('settings','latencyCheckCount') if config.has_option('settings','latencyCheckCount') else "",
                "latencyCheckBucket": config.get('settings','latencyCheckBucket') if config.has_option('settings','latencyCheckBucket') else "npc",
                "logLevel": config.get('settings','logLevel') if config.has_option('settings','logLevel') else "info",
            },
            "influxdb": {
                "influxHost": config.get('influxdb', 'host') if config.has_option('influxdb','host') else "",
                "influxToken": config.get('influxdb', 'token') if config.has_option('influxdb','token') else "",
                "influxOrg": config.get('influxdb', 'org') if config.has_option('influxdb','org') else "",
            }
            
        }
        
        return config
        
        