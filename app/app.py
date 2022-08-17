import utils.getConfig as conf
import utils.logging as log
import utils.threadHelper as threadHelper
import time

config = conf.getConfig("configFile")


def main():
    threadHandler = threadHelper.ThreadHelper()

    if not threadHandler.initFeatureThreads(config=config):
        log.writeLog(f"No features enabled, exiting...", "ERROR", "stdout")
        exit(0)

    while (True):
        for key in config['features']:
            if config['features'][key] == 'True':
                try:
                    if not threadHandler.isThreadAlive(key):
                        threadHandler.startThread(key)
                except Exception as e:
                    log.writeLog(
                        f"Couldnt start {key} Thread \n with Error {e}", "ERROR", "stdout")

        time.sleep(10)


if __name__ == "__main__":
    main()
