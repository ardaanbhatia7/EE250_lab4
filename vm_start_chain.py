import paho.mqtt.client as mqtt
import time

BROKER = "172.20.10.3"
USERNAME = "rochlani"       # replace with your USC username
TOPIC_PING = f"{USERNAME}/ping"
TOPIC_PONG = f"{USERNAME}/pong"

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))
    client.subscribe(TOPIC_PONG)
    client.message_callback_add(TOPIC_PONG, on_message_from_pong)

def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_pong(client, userdata, message):
    num = int(message.payload.decode())
    print("Custom callback - PONG received:", num)
    num += 1
    time.sleep(1)
    client.publish(TOPIC_PING, num)
    print("Published to PING:", num)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    client.connect(host=BROKER, port=1883, keepalive=60)

    client.loop_start()
    time.sleep(1)

    start_num = 0
    client.publish(TOPIC_PING, start_num)
    print("Starting chain with", start_num)

    while True:
        time.sleep(1)
