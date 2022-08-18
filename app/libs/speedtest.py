import re
import subprocess
import json
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
    speedtest = subprocess.Popen(
        '/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE)
    speedtest = speedtest.stdout.read().decode('utf-8')

    ping = re.search('Latency:\s+(.*?)\s', speedtest, re.MULTILINE)
    download = re.search('Download:\s+(.*?)\s', speedtest, re.MULTILINE)
    upload = re.search('Upload:\s+(.*?)\s', speedtest, re.MULTILINE)
    jitter = re.search('Latency:.*?jitter:\s+(.*?)ms', speedtest, re.MULTILINE)

    ping = ping.group(1)
    download = download.group(1)
    upload = upload.group(1)
    jitter = jitter.group(1)

    return prepResults(ping,download,upload,)

def speedtestFastCom(hostname):
    
    ping = pingHost.pingHost(hostname, 1)
    
    speedtest = fastcli.run()
    
    return prepResults(ping['rtt_avg'],speedtest,0)


def speedtestIperf3(hostname, port):

    ping = pingHost.pingHost(hostname, 1)

    speedtest = subprocess.Popen(
        f"iperf3 -c {hostname} -p {port} -J", shell=True, stdout=subprocess.PIPE)
    speedtest = speedtest.stdout.read().decode('utf-8')

    result = json.loads(speedtest)

    return prepResults(ping['rtt_avg'],result['end']['sum_received']['bits_per_second']\
        ,result['end']['sum_sent']['bits_per_second'])

