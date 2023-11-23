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

ssid = 'iPhone'
password = '11281128'
#mqtt_server = 'test.mosquitto.org'
#mqtt_topic = 'rrc/iot/test'

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
    It reads data from the moisture sensor and publishes it in JSON format
    and under separate topics for each data point.
    """
    try:
        data = moisture_sensor.moisture()
        if data:
            # JSON data publishing
            json_data = ujson.dumps(data)
            client.publish(TOPIC_BASE + "json", json_data)

            # Publishing individual data points
            client.publish(TOPIC_BASE + "raw", str(data['raw']))
            client.publish(TOPIC_BASE + "percent", "{:.2f}%".format(data['percent']))
            client.publish(TOPIC_BASE + "volts", "{:.3f}V".format(data['volts']))
            print("main.py: Data published successfully.")
            print("main.py: Actual moisture sensor data:", data)
    except Exception as e:
        print("main.py: publish_sensor_data: Error:", e)

# Timer setup for periodic data publishing
try:
    timer = Timer(-1)
    timer.init(mode=Timer.PERIODIC, period=10000, callback=publish_sensor_data)
except Exception as e:
    print("main.py: timer_setup: Error:", e)
