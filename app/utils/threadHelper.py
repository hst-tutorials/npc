import threading

#from . import getConfig as conf
from utils import config as conf
from . import logging as log

from libs import bandwidth
from libs import ping

#Import config from helper class
config = conf.Config()
config = config.parseConfig()


class ThreadHelper:

    THREADS = config

    #helper function to start thread, if it does not exist, create it and save it into the THREADS variable
    def startThread(self, key) -> None:
        if self.THREADS[key]['thread'] is not None:
            self.THREADS[key]['thread'] = self.getFeatureThread(
                key, self.THREADS[key]['name'], self.THREADS[key]['args'])
        self.THREADS[key]['thread'].start()

    def getFeatureThread(self, featureKey: str, name: str, args) -> threading.Thread:
        thread = threading.Thread(target=self.THREADS[featureKey]['module'],
                                  name=name, args=(args[0], args[1], args[2], args[3]))

        if thread is None:
            raise Exception("No Thread with given config was found")

        return thread

    #function to init threads when the application is starting
    def initFeatureThreads(self, config) -> bool:
        featureEnabled = False

        #check if module is enabled, then create the thread, start it and save it into the THREADS variable
        for key in config:
            if config[key]['enabled'] and 'module' in config[key]:
                try:
                    featureEnabled = True
                    thread = self.getFeatureThread(
                        key, name=self.THREADS[key]['name'], args=self.THREADS[key]['args'])
                    self.THREADS[key].update({'thread': thread})
                    thread.start()
                except Exception as e:
                    log.writeLog(
                        f"Couldnt init {key} Thread!\n with Error {e}", "ERROR", "stdout")

        return featureEnabled

    #check if thread is alive and return its status
    def isThreadAlive(self, key) -> bool:
        return self.THREADS[key]['thread'] is not None and self.THREADS[key]['thread'].is_alive()
