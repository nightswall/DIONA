import paho.mqtt.client as mqtt
import time

def start_publisher(broker, topic, log, count):
    client = mqtt.Client("publisher")

    print("Connecting to broker:", broker)
    client.connect(broker)
    client.loop_start()

    for _ in range(count):
        print("Sending data...")
        client.publish(topic, log)
        time.sleep(3)

    client.loop_stop()
    client.disconnect()
