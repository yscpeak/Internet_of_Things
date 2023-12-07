"""
This module connects to AWS IoT via MQTT over SSL, 
periodically sending sensor data in JSON format from ESP32.
"""

from umqtt.simple import MQTTClient
import time
from machine import Timer
import json
from sensor import Sensor
from sensor import get_sensor_data

def setup_aws():
    """Setup AWS with robust error handling."""
    try:
        # Setup AWS SSL
        KEY_PATH = "2deec3310c0647a740895e9bb8a3d45abc413a38adb276c4e5c8affb5c47f39a-private.pem.key"
        CERT_PATH = "2deec3310c0647a740895e9bb8a3d45abc413a38adb276c4e5c8affb5c47f39a-certificate.pem.crt"
        try:
            with open(KEY_PATH, "r") as f:
                key = f.read()
            with open(CERT_PATH, "r") as f:
                cert = f.read()
        except Exception as e:
            print("main.py:setup_aws:read_ssl_certs:error:", e)
            raise

        # Setup AWS parameters
        CLIENT_ID = "Firebeetle"
        HOST = "a32ypeqphfvdeq-ats.iot.us-east-1.amazonaws.com"
        PORT = 8883
        SSL_PARAMS = {"key": key, "cert": cert, "server_side": False}

        # Setup MQTT
        global client
        client = MQTTClient(client_id=CLIENT_ID,
                            server=HOST,
                            port=PORT,
                            keepalive=10000,
                            ssl=True,
                            ssl_params=SSL_PARAMS)
        client.connect()
        print("Connected to AWS")
    except Exception as e:
        print("main.py:setup_aws:error:", e)
        raise

def publish_sensor_data(timer):
    """Publish sensor data with error handling."""
    try:
        data = get_sensor_data()
        payload = json.dumps({"state": {"reported": data}})
        client.publish("$aws/things/Firebeetle/shadow/update", payload)
        print("Published:", payload)
    except Exception as e:
        print("main.py:publish_sensor_data:error:", e)

def main():
    """Main function with error handling."""
    try:
        setup_aws()
        timer = Timer(0)
        timer.init(period=10000, mode=Timer.PERIODIC, callback=publish_sensor_data)
    except Exception as e:
        print("main.py:main:error:", e)

if __name__ == "__main__":
    """
    Entry point of the script. Calls the main function and includes global error handling.
    """
    try:
        main()
    except Exception as e:
        print("main.py:global_scope:error:", e)