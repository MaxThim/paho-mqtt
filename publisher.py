import paho.mqtt.client as mqtt_client

client = mqtt_client.Client()

if client.connect("localhost", 1883, 60) != 0:
    print("Connection failed")
    exit(1)

client.publish("test/status", "Hello, World!", 0)

client.disconnect()