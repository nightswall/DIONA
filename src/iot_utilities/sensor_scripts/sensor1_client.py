import random
import paho.mqtt.client as mqtt
import sys
import time
# example: python sensor1_client.py 10.0.0.4
# Set the server IP from argument passed to the script
server_ip = sys.argv[1]
# print connecting to server_ip
print("Connecting to " + server_ip)
# Set the topic for the sensor readings
topic = "sensor/temperature"

# Function to generate a random temperature reading
def generate_reading():
    return random.uniform(20, 30)

# Function to send the temperature reading to the MQTT broker
def send_reading(client, reading):
    client.publish(topic, reading)

# Create the MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(server_ip , 1883, 60)

# Generate and send a random temperature reading every 5 seconds
while True:
    reading = generate_reading()
    send_reading(client, reading)
    time.sleep(5)

# Disconnect from the MQTT broker
client.disconnect()
