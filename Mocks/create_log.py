class LogType:
    STATUS, ERROR, AUTHENTICATION, CONFIGURATION, MEMORY = range(5)

def create_log(type, timestamp, text):
    return {
        "type": type,
        "timestamp": timestamp,
        "text": text,
    }
