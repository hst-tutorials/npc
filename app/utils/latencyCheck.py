#!/usr/bin/python3
from libs import influxdb as influx
from libs import ping
from . import getConfig as conf
from . import logging as log

import json


def main(name, hosts, count):

    config = conf.getConfig("configFile")

    influx_measurement = 'latency_check'

    for hostname in json.loads(hosts):

        log.writeLog(
            f"Latency check starting for host {hostname}", "INFO", "stdout")

        pingData = ping.pingHost(hostname, count)

        # format results into data for influxdb
        data = [
            {
                "measurement": influx_measurement,
                "tags": {
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

        log.writeLog(f"Latency check finished", "INFO", "stdout")

        # write data to influx
        if config['influxdb']['enabled'] == "True":
            log.writeLog("Writing data to influxdb", "INFO", "stdout")
            influx.writeToInflux(
                data, config['settings']['latencyCheckBucket'])
        else:
            print(data)
