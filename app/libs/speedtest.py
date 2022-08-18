import re
import subprocess
import json
import iperf3
import speedtest as speedtestCli
from . import ping as pingHost
from . import fastcli


def prepResults(ping, download,upload):
    
    result = {
        "ping": ping,
        "download": download,
        "upload": upload,
    }
    
    return result

def speedtestOokla():
    
    speedtest = speedtestCli.Speedtest()
    speedtest.get_best_server()
    
    
    speedtest.download(threads=4)
    speedtest.upload(threads=4)

    return prepResults(speedtest.results.ping,speedtest.results.download,speedtest.results.upload)

def speedtestFastCom(hostname):
    
    ping = pingHost.pingHost(hostname, 1)
    
    speedtest = fastcli.run()
    
    return prepResults(ping['rtt_avg'],speedtest,0)


def speedtestIperf3(hostname, port):
    
    ping = pingHost.pingHost(hostname, 1)
    
    speedtest = iperf3.Client()
    speedtest.server_hostname = hostname
    speedtest.port = port
    speedtest.zerocopy = True
    speedtest.duration = 10
    
    speedtest = speedtest.run()    

    return prepResults(ping['rtt_avg'],speedtest.received_Mbps\
        ,speedtest.sent_Mbps)

