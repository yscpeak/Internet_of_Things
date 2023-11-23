"""
This module handles connecting an ESP32 to an MQTT broker, 
reading moisture data from a sensor, and publishing it periodically.
"""

#import machine
import ntptime
import time
import network
import ujson
from umqtt.simple import MQTTClient
# import umqtt.simple as mqtt
from sensor import Sensor # import sensor.py
from machine import Timer

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_attempts = 10
    attempts = 0
    while not wlan.isconnected() and attempts < max_attempts:
        time.sleep(1)
        attempts += 1

    if wlan.isconnected():
        print("main.py: Connected to WiFi:", wlan.ifconfig())
    else:
        print("main.py: Failed to connect to WiFi")
        return False
    return True

# Variable initialization
try:
    sensor_pin = 36  # GPIO pin for the moisture sensor
    MQTT_CLIENT_ID = "YiSiangProject1"
    MQTT_BROKER = "test.mosquitto.org"
    #MQTT_BROKER = "broker.hivemq.com"
    TOPIC_BASE = "mytopic/iot/moisture/"
except Exception as e:
    print("main.py: variable_initialization: Error:", e)

# Sensor and MQTT Client Setup
if connect_to_wifi(ssid, password):
    try:
        moisture_sensor = Sensor(sensor_pin)  # Initialize the moisture sensor
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)  # MQTT client setup
        client.connect()
        print("main.py: Successfully connected to MQTT broker:", MQTT_BROKER)
    except Exception as e:
        print("main.py: Error in MQTT setup or connection:", e)

def publish_sensor_data(t):
    """
    Publishes moisture data to an MQTT broker.
    This function is called periodically by a timer.
    """
    try:
        json_data = moisture_sensor.moisture()  # This is now a JSON string
        data = ujson.loads(json_data)  # Convert the JSON string back to a dictionary

        if data:
            # Publishing individual data points with timestamp
            raw_data = "Raw: {} @ {}".format(data['raw'], data['timestamp'])
            percent_data = "Percent: {:.2f}% @ {}".format(data['percent'], data['timestamp'])
            volts_data = "Voltage: {:.3f}V @ {}".format(data['volts'], data['timestamp'])

            client.publish(TOPIC_BASE + "raw", raw_data)
            client.publish(TOPIC_BASE + "percent", percent_data)
            client.publish(TOPIC_BASE + "volts", volts_data)

            print("main.py: Data published successfully.")
            print("main.py: Actual moisture sensor data:", data)
            #print("Raw: {} @ {}".format(data['raw'], data['timestamp']))
            #print("Percent: {:.2f}% @ {}".format(data['percent'], data['timestamp']))
            #print("Voltage: {:.3f}V @ {}".format(data['volts'], data['timestamp'])) 
        
    except Exception as e:
        print("main.py: publish_sensor_data: Error:", e)

# Timer setup for periodic data publishing
try:
    timer = Timer(-1)
    timer.init(mode=Timer.PERIODIC, period=10000, callback=publish_sensor_data)
except Exception as e:
    print("main.py: timer_setup: Error:", e)
