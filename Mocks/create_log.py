import datetime
import time

class LogType:
    STATUS, ERROR, AUTHENTICATION, CONFIGURATION, MEMORY = range(5)

def create_log(type, date, text):
    timestamp = time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y %H:%M").timetuple())
    return {
        "type": type,
        "timestamp": timestamp,
        "text": text,
    }
