"""
This module uses MQTT and threading to fetch sensor data from AWS IoT Core 
and display it in real-time with Matplotlib.
"""
import paho.mqtt.client as mqtt
import json
import ssl
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from queue import Queue
import threading

# AWS and MQTT configuration
broker = "a32ypeqphfvdeq-ats.iot.us-east-1.amazonaws.com"
port = 8883
topic = "$aws/things/Firebeetle/shadow/get/accepted"
client_id = "Firebeetle"
cert_file = "2deec3310c0647a740895e9bb8a3d45abc413a38adb276c4e5c8affb5c47f39a-certificate.pem.crt"
key_file = "2deec3310c0647a740895e9bb8a3d45abc413a38adb276c4e5c8affb5c47f39a-private.pem.key"
ca_file = "AmazonRootCA1.pem"

# Data Storage
data = []

# Flag to indicate when to update the plot
update_required = False

# Thread-safe queue for data sharing
data_queue = Queue()

# MQTT Callback Function
def on_connect(client, userdata, flags, rc):
    """
    Callback for when the client receives a response from the server.
    Subscribes to the AWS IoT Core topic if the connection is successful.
    """
    if rc == 0:
        print("Connected to AWS IoT Core")
        client.subscribe(topic)
    else:
        print("Connection failed with code %d." % rc)

def on_message(client, userdata, msg):
    """
    Callback for when a PUBLISH message is received from the server.
    """
    print("Received a message.")
    payload = json.loads(msg.payload)
    moisture = payload["state"]["reported"]["moisture"]
    print(f"Moisture: {moisture}")
    timestamp = datetime.now()
    data_queue.put((timestamp, moisture))
    global update_required
    update_required = True

# Update Matplotlib Plot
def update_plot():
    """
    Updates the Matplotlib plot with the latest sensor data.
    """
    global data, update_required
    print("Current data:", data)
    one_hour_ago = datetime.now() - timedelta(hours=1)
    filtered_data = [(t, m) for t, m in data if t > one_hour_ago]
    times, values = zip(*filtered_data) if filtered_data else ([], [])
    plt.clf()
    plt.plot(times, values)
    plt.xlabel('Time')
    plt.ylabel('Moisture (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.draw()
    plt.pause(1)
    update_required = False  # Reset the flag

# MQTT Client Thread
def mqtt_client_thread():
    """
    Handles the MQTT connection, message subscription, and data reception in a separate thread.
    """
    global update_required
    client = mqtt.Client(client_id)
    client.tls_set(ca_certs=ca_file, certfile=cert_file, keyfile=key_file,
                   cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port)
    client.loop_start()

    while True:
        if not data_queue.empty():
            timestamp, moisture = data_queue.get()
            data.append((timestamp, moisture))
        client.publish("$aws/things/Firebeetle/shadow/get", "{}")
        time.sleep(10)  # Send request every 10 seconds
        if update_required:
            update_plot()

    client.loop_stop()

# Initialize Matplotlib in the main thread
plt.ion()
plt.show()

if __name__ == "__main__":
    """
    Starts the MQTT client thread and runs the main loop for updating the plot.
    """
    client_thread = threading.Thread(target=mqtt_client_thread)
    client_thread.start()

    while True:
        time.sleep(1)  # Adjust the sleep time as needed
        if update_required:
            update_plot()  # Plot update is called in the main thread
