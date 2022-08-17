from datetime import datetime



def writeLog(message, level, target):
        
    if target == "stdout":
        dt = datetime.now()
        dt = dt.strftime("[%d-%m-%Y %H:%M:%S]")
        print(f"{dt} | {level} | {message}")
    #Todo File-Logging