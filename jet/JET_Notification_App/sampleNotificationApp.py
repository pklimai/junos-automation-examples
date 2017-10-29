#!/usr/bin/python3

import paho.mqtt.client

def mqtt_callback(client, user_data, message):
    print("Message with topic {} received: {}"
          .format(message.topic, str(message.payload.decode("utf-8"))))

DEVICE1 = "10.254.0.41"
TOPIC = "/junos/events/syslog/LOGIN_INFORMATION"

print("Connecting to {} and listening to topic {}".format(DEVICE1, TOPIC))
client = paho.mqtt.client.Client("P1")
client.on_message=mqtt_callback
client.connect(DEVICE1)
client.loop_start()
client.subscribe(TOPIC)
client.publish(TOPIC, "*** This test message was published by client ***")

print("Press Enter to stop")
input()
client.loop_stop()
