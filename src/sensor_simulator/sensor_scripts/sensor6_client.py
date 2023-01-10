# sensor6_client.py
import random
import paho.mqtt.client as mqtt
import sys
import time

# Set the server IP from argument passed to the script
server_ip = sys.argv[1]

# Set the topic for the sensor readings
topic = "sensor/microphone"

# Function to generate a random microphone reading
def generate_reading():
    return random.uniform(0, 100)

# Function to send the microphone reading to the MQTT broker
def send_reading(client, reading):
    client.publish(topic, reading)

# Create the MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(server_ip , 1883, 60)

# Generate and send a random microphone reading every 5 seconds
while True:
    reading = generate_reading()
    send_reading(client, reading)
    time.sleep(5)

# Disconnect from the MQTT broker
client.disconnect()

