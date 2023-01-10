import paho.mqtt.client as mqtt

def start_subscriber(broker, topic, on_message):
    client = mqtt.Client("subscriber")
    client.on_message = on_message

    print("Connecting to broker:", broker)
    client.connect(broker)
    client.loop_start()

    client.subscribe(topic)

def disconnect_client(client):
    client.loop_stop()
    client.disconnect()
