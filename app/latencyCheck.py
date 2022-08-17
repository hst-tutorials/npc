#!/usr/bin/python3
import json
from pydoc import doc
import pingparsing
import sys, getopt
import libs.influxdb as influx
import libs.ping as ping
import libs.getConfig as conf
import libs.logging as log


def main(hosts,count):

    config = conf.getConfig("configFile")

    influx_measurement = 'latency_check'
    
    for hostname in hosts:
    
        log.writeLog(f"Latency check starting for host {hostname}","INFO","stdout")
    
        pingData = ping.pingHost(hostname, count)
        
        #format results into data for influxdb
        data = [
        {
            "measurement" : influx_measurement,
            "tags" : {
                "host": hostname
            },
            "fields": {
                "destination": pingData['destination'],
                "packet_transmit": pingData['packet_transmit'],
                "packet_loss_count": pingData['packet_loss_count'],
                "packet_loss_rate": pingData['packet_loss_rate'],
                "rtt_min": pingData['rtt_min'],
                "rtt_avg": pingData['rtt_avg'],
                "rtt_max": pingData['rtt_mdev'],
                "packet_duplicate_count": pingData['packet_duplicate_count'],
                "packet_duplicate_rate": pingData['packet_duplicate_rate']
            }
        }

        ]
        
        log.writeLog(f"Latency check finished","INFO","stdout")

        #write data to influx
        if config['features']['influxDBEnabled'] == "True":
            influx.writeToInflux(data,config['settings']['latencyCheckBucket'])
        else:
            print(data)