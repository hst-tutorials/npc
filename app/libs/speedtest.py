import re
import subprocess
import json
from . import ping as pingHost


def speedtestOokla():
    response = subprocess.Popen(
        '/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE)
    response = response.stdout.read().decode('utf-8')

    ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
    download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
    upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
    jitter = re.search('Latency:.*?jitter:\s+(.*?)ms', response, re.MULTILINE)

    ping = ping.group(1)
    download = download.group(1)
    upload = upload.group(1)
    jitter = jitter.group(1)

    result = {
        "ping": ping,
        "download": download,
        "upload": upload,
    }

    return result


def speedtestIperf3(hostname, port):

    ping = pingHost.pingHost(hostname, 1)

    speedtest = subprocess.Popen(
        f"iperf3 -c {hostname} -p {port} -J", shell=True, stdout=subprocess.PIPE)
    speedtest = speedtest.stdout.read().decode('utf-8')

    result = json.loads(speedtest)

    result = {
        "ping": ping['rtt_avg'],
        "download": result['end']['sum_received']['bits_per_second'],
        "upload": result['end']['sum_sent']['bits_per_second'],
    }

    return result
