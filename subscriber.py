import paho.mqtt.client as mqtt_client

MQTT_BROKER = "mqtt.eclipseprojects.io"

client = mqtt_client.Client()

client.connect(MQTT_BROKER, 1883, 60)

def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print("Connection failed")
        exit(1)

client.subscribe("test/status")