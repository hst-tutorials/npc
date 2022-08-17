#!/usr/bin/python3
import json
from pydoc import doc
import sys, getopt
import libs.influxdb as influx
import libs.speedtest as speedtest
import libs.getConfig as conf
import libs.logging as log
import time

def main(speedtestType,hostname,port):

    config = conf.getConfig("configFile")

    log.writeLog(f"Speedtest with type {speedtestType} starting","INFO","stdout")

    #differ between different speedtest types, e.g. speedtest.net or iperf3
    if speedtestType == "speedtest.net":
        hostname = "speedtest.net"
        data = speedtest.speedtestOokla()
        bucketName = config['settings']['ooklaBucket']
        
    elif speedtestType == "iperf3":
        data = speedtest.speedtestIperf3(hostname,port)
        bucketName = config['settings']['iPerf3Bucket']
        
    else:
        log.writeLog(f"Please enter correct speedtest type","ERROR","stdout")
            
    data = [
        {
            "measurement" : speedtestType,
            "tags" : {
                "host": hostname
            },
            "fields": {
                "download": float(data['download']),
                "upload": float(data['upload']),
                "ping": float(data['ping']),
            }
        }
    ]
    
    log.writeLog(f"Speedtest with type {speedtestType} finished","INFO","stdout")
    
    if config['features']['influxDBEnabled'] == "True":
        influx.writeToInflux(data,bucketName)
    else:
        print(data)
    
    
    
    return True