import libs.getConfig as conf
import libs.logging as log
import os
import subprocess
import time
import speedtest
import latencyCheck
import threading

def main():
    config = conf.getConfig("configFile")
        
    while(True):
        
        if (config['features']['OoklaSpeedtestEnabled'] == "True"):
            if 'OoklaSpeedtestThread' in locals() and not OoklaSpeedtestThread.is_alive():
                OoklaSpeedtestThread = threading.Thread(target=speedtest.main, name="OoklaSpeedtest", args=("speedtest.net","",""))
                OoklaSpeedtestThread.start()
            elif not 'OoklaSpeedtestThread' in locals():
                OoklaSpeedtestThread = threading.Thread(target=speedtest.main, name="OoklaSpeedtest", args=("speedtest.net","",""))
                OoklaSpeedtestThread.start()
            
        if (config['features']['iPerf3SpeedtestEnabled'] == "True"):
            if 'iPerfSpeedtestThread' in locals() and not iPerfSpeedtestThread.is_alive():
                iPerfSpeedtestThread = threading.Thread(target=speedtest.main, name="iPerfSpeedtest", args=("iperf3",config['settings']['iPerf3Hostname'],config['settings']['iPerf3Port']))
                iPerfSpeedtestThread.start()
            elif not 'iPerfSpeedtestThread' in locals():
                iPerfSpeedtestThread = threading.Thread(target=speedtest.main, name="iPerfSpeedtest", args=("iperf3",config['settings']['iPerf3Hostname'],config['settings']['iPerf3Port']))
                iPerfSpeedtestThread.start()
        
        if (config['features']['latencyCheckEnabled'] == "True"):
            if 'latencyCheckThread' in locals() and not latencyCheckThread.is_alive():
                latencyCheckThread = threading.Thread(target=latencyCheck.main, name="latencyCheck", args=(config['settings']['latencyCheckHostnames'],config['settings']['latencyCheckCount']))
                latencyCheckThread.start()
            elif not 'latencyCheckThread' in locals():
                latencyCheckThread = threading.Thread(target=latencyCheck.main, name="latencyCheck", args=(config['settings']['latencyCheckHostnames'],config['settings']['latencyCheckCount']))
                latencyCheckThread.start()
                
                            
        if (config['features']['OoklaSpeedtestEnabled'] == "False" and config['features']['iPerf3SpeedtestEnabled'] == "False" and config['features']['iPerf3SpeedtestEnabled'] == "False"):
            print("No features enabled, exiting...")
            log.writeLog(f"No features enabled, exiting...","ERROR","stdout")
            exit(0)
            
        time.sleep(10)

    
if __name__ == "__main__":
   main()