import json
from create_log import *
from mock_publisher import *
from mock_subscriber import *

date = "01/12/2011 00:00"
log = create_log(LogType.STATUS, date, "command")
log_encoded = json.dumps(log) # encode dictionary to json

broker = "test.mosquitto.org"
topic = "test/diona"

def on_message(client, userdata, message):
    message_string = str(message.payload.decode("utf-8", "ignore"))
    log_decoded = json.loads(message_string) # decode incoming JSON to object
    print("message ", log_decoded)

start_subscriber(broker, topic, on_message)
start_publisher(broker, topic, log_encoded, 3)
