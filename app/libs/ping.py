import pingparsing
import json

def pingHost(hostname, count):
    #setup ping parsing lib
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = hostname
    transmitter.count = count
    result = transmitter.ping()

    #write results into readable json
    return json.loads(json.dumps(ping_parser.parse(result).as_dict(), indent=4))