import paho.mqtt.client as mqtt
import time
import json

HOST_NAME = "localhost"

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def run():
    client = mqtt.Client()
    client.connect(HOST_NAME)
    client.on_message = on_message
    client.subscribe("sensors/#")
    while True:
        client.loop()

run()