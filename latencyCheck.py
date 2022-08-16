#!/usr/bin/python3
import json
from pydoc import doc
import pingparsing
import sys, getopt
import libs.influxdb as influx

def main(argv):

    hostname = ''
    interval = ''


    try:
        opts, args = getopt.getopt(argv,"h:i:",["host","interval"])
    except:
        print ('latencyCheck.py -h <Hostname> -i <interval>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--host'):
            hostname = arg
        elif opt in ('-i', '--interval'):
            interval = int(arg)

    influx_measurement = 'latency_check'
    

    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = hostname
    transmitter.count = interval
    result = transmitter.ping()

    result = json.loads(json.dumps(ping_parser.parse(result).as_dict(), indent=4))

    while(True):
        data = [
        {
            "measurement" : influx_measurement,
            "tags" : {
                "host": hostname
            },
            "fields": {
                "destination": result['destination'],
                "packet_transmit": result['packet_transmit'],
                "packet_loss_count": result['packet_loss_count'],
                "packet_loss_rate": result['packet_loss_rate'],
                "rtt_min": result['rtt_min'],
                "rtt_avg": result['rtt_avg'],
                "rtt_max": result['rtt_mdev'],
                "packet_duplicate_count": result['packet_duplicate_count'],
                "packet_duplicate_rate": result['packet_duplicate_rate']
            }
        }

        ]

        influx.writeToInflux(data)


    

if __name__ == "__main__":
   main(sys.argv[1:])