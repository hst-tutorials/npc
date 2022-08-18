#import utils.getConfig as conf
import utils.config as conf
import utils.logging as log
import utils.threadHelper as threadHelper
import time

#config = conf.getConfig("configFile")

config = conf.Config()
config = config.parseConfig()


def main():

    threadHandler = threadHelper.ThreadHelper()

    if not threadHandler.initFeatureThreads(config=config):
        log.writeLog(f"No features enabled, exiting...", "ERROR", "stdout")
        exit(0)

    while (True):
        for key in config:
            if config[key]['enabled'] and 'module' in config[key]:
                try:
                    if not threadHandler.isThreadAlive(key):
                        threadHandler.startThread(key)
                except Exception as e:
                    log.writeLog(
                        f"Couldnt start {key} Thread \n with Error {e}", "ERROR", "stdout")

        time.sleep(10)


if __name__ == "__main__":
    main()
