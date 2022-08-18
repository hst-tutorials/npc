import iperf3
import speedtest as speedtestCli
from . import ping as pingHost
from . import fastcli
from . import influxdb as influx
from utils import logging as log
import time


def prepResults(measurement, hostname, ping, download, upload):

    result = [
        {
            "measurement": measurement,
            "tags": {
                "host": hostname
            },
            "fields": {
                "ping": float(ping),
                "download": float(download),
                "upload": float(upload),
            }
        }
    ]

    return result


def ookla(config, interval, hostname, port):

    speedtestType = "speedtest.net"

    speedtest = speedtestCli.Speedtest()
    speedtest.get_best_server()

    speedtest.download(threads=4)
    speedtest.upload(threads=4)

    log.writeLog(
        f"Speedtest with type {speedtestType} finished", "INFO", "stdout")

    results = prepResults(speedtestType, hostname, speedtest.results.ping,
                          speedtest.results.download, speedtest.results.upload)

    influx.writeToInflux(config, results, config['ookla']['bucket'])

    time.sleep(interval)


def fastCom(config, interval, hostname, port):

    speedtestType = "fast.com"

    ping = pingHost.pingHost(hostname, 1)

    speedtest = fastcli.run()

    results = prepResults(speedtestType, hostname,
                          ping['rtt_avg'], speedtest, 0)
    
    log.writeLog(
        f"Speedtest with type {speedtestType} finished", "INFO", "stdout")

    influx.writeToInflux(config, results, config['fastCom']['bucket'])

    time.sleep(interval)


def iPerf3(config, interval, hostname, port):

    speedtestType = "iPerf3"

    ping = pingHost.pingHost(hostname, 1)

    speedtest = iperf3.Client()
    speedtest.server_hostname = hostname
    speedtest.port = port
    speedtest.zerocopy = True
    speedtest.duration = 10

    speedtest = speedtest.run()

    results = prepResults(speedtestType, hostname,
                          ping['rtt_avg'], speedtest.received_Mbps, speedtest.sent_Mbps)
    
    log.writeLog(
        f"Speedtest with type {speedtestType} finished", "INFO", "stdout")

    influx.writeToInflux(config, results, config['iperf3']['bucket'])

    time.sleep(interval)
