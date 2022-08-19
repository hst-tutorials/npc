import utils.config as conf
import utils.logging as log
import utils.threadHelper as threadHelper
import time

#Import config from helper class
config = conf.Config()
config = config.parseConfig()


def main():

    #create threadhelper object to keep track of running feature threads
    threadHandler = threadHelper.ThreadHelper()

    #if the init thread function returns false, no features are enabled
    if not threadHandler.initFeatureThreads(config=config):
        log.writeLog(f"No features enabled, exiting...", "ERROR", "stdout")
        exit(0)

    while (True):
        for key in config:
            #recheck if feature is enabled
            if config[key]['enabled'] and 'module' in config[key]:
                #try to start the thread if it isn't alive anymore -> feature has finished working
                try:
                    if not threadHandler.isThreadAlive(key):
                        threadHandler.startThread(key)
                except Exception as e:
                    log.writeLog(
                        f"Couldnt start {key} Thread \n with Error {e}", "ERROR", "stdout")

        time.sleep(10)


if __name__ == "__main__":
    main()
