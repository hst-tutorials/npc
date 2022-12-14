import pingparsing
import json
from . import influxdb as influx
from utils import logging as log
import time

# function to parse the given data into influx readable format (json)
def prepResults(measurement, hostname, data):

    data = [
        {
            "measurement": measurement,
            "tags": {
                "host": hostname
            },
            "fields": {
                "destination": data['destination'],
                "packet_transmit": data['packet_transmit'],
                "packet_loss_count": data['packet_loss_count'],
                "packet_loss_rate": data['packet_loss_rate'],
                "rtt_min": data['rtt_min'],
                "rtt_avg": data['rtt_avg'],
                "rtt_max": data['rtt_mdev'],
                "packet_duplicate_count": data['packet_duplicate_count'],
                "packet_duplicate_rate": data['packet_duplicate_rate']
            }
        }

    ]

    return data

# helper function to ping host and return the results (used in iperf3 and 
# fast.com speedtests as well as latency check)
def pingHost(hostname, count):
    pingParser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = hostname
    transmitter.count = count
    results = transmitter.ping()

    # write results into readable json
    return json.loads(json.dumps(pingParser.parse(results).as_dict(), indent=4))


def latency(config, interval, hostnames, count):

    # loop through hostnames as multiple hosts can be checked
    for hostname in hostnames:

        measurement = "latency"

        log.writeLog(
            f"Latency check starting for host {hostname}", "INFO", "stdout")

        results = pingHost(hostname, count)

        log.writeLog(
            f"Latency check finished for host {hostname}", "INFO", "stdout")

        influx.writeToInflux(config, prepResults(
            measurement, hostname, results), config['latency']['bucket'])

        # sleep for given interval (set in config.json)
        time.sleep(interval)
