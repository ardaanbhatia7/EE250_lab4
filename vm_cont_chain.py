import paho.mqtt.client as mqtt
import time

BROKER = "172.20.10.3"
USERNAME = "rochlani"
TOPIC_PING = f"{USERNAME}/ping"
TOPIC_PONG = f"{USERNAME}/pong"

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))
    client.subscribe(TOPIC_PING)
    client.message_callback_add(TOPIC_PING, on_message_from_ping)

def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_ping(client, userdata, message):
    num = int(message.payload.decode())
    print("Custom callback - PING received:", num)
    num += 1
    time.sleep(1)
    client.publish(TOPIC_PONG, num)
    print("Published to PONG:", num)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    client.connect(host=BROKER, port=1883, keepalive=60)
    client.loop_forever()
