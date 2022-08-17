import threading

from . import getConfig as conf
from . import logging as log

from . import speedtestFetcher
from . import latencyCheck

config = conf.getConfig("configFile")


class ThreadHelper:

    THREADS = {
        'ooklaspeedtest': {
            'name': "OoklaSpeedtest",
            'args': ["speedtest.net", "", ""],
            'thread': None,
            'module': speedtestFetcher
        },
        'iperf3speedtest': {
            'name': "iPerfSpeedtest",
            'args': ["iperf3", config['settings']['iperf3hostname'], config['settings']['iperf3port']],
            'thread': None,
            'module': speedtestFetcher
        },
        'latencycheck': {
            'name': "latencyCheck",
            'args': ["latencyCheck", config['settings']['latencycheckhostnames'], config['settings']['latencycheckcount']],
            'thread': None,
            'module': latencyCheck
        }
    }

    def startThread(self, key):
        if self.THREADS[key]['thread'] is not None:
            self.THREADS[key]['thread'] = self.getFeatureThread(
                key, self.THREADS[key]['name'], self.THREADS[key]['args'])
        self.THREADS[key]['thread'].start()

    def getFeatureThread(self, featureKey: str, name: str, args) -> threading.Thread:
        thread = threading.Thread(target=self.THREADS[featureKey]['module'].main,
                                  name=name, args=(args[0], args[1], args[2]))

        if thread is None:
            raise Exception("No Thread with given config was found")

        return thread

    def initFeatureThreads(self, config) -> bool:
        featureEnabled = False

        for key in config['features']:
            if config['features'][key] == 'True':
                try:
                    featureEnabled = True
                    thread = self.getFeatureThread(
                        key, name=self.THREADS[key]['name'], args=self.THREADS[key]['args'])
                    self.THREADS[key]['thread'] = thread
                    thread.start()
                except Exception as e:
                    log.writeLog(
                        f"Couldnt init {key} Thread!\n with Error {e}", "ERROR", "stdout")

        return featureEnabled

    def isThreadAlive(self, key) -> bool:
        return self.THREADS[key]['thread'] is not None and self.THREADS[key]['thread'].is_alive()
