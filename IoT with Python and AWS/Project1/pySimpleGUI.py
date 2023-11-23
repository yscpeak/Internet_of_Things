"""
This module handles the creation of a simple graphical user interface using PySimpleGUI. 
It displays sensor data fetched from an external source and updates the display periodically.
"""

import PySimpleGUI as sg
import paho.mqtt.client as mqtt
import json

class SensorDataDisplay:
    """Class to setup and manage GUI window for displaying sensor data."""

    def __init__(self):
        """Initialize the GUI layout, window, and MQTT client."""
        try:
            self.layout = [
                [sg.Text("Sensor Data", font=("Helvetica", 16))],
                [sg.Text("Raw:", size=(8, 1)), sg.Text("Waiting...", key="RAW")],
                [sg.Text("Percent:", size=(8, 1)), sg.Text("Waiting...", key="PERCENT")],
                [sg.Text("Volts:", size=(8, 1)), sg.Text("Waiting...", key="VOLTS")],
                [sg.Button("Exit")]
            ]
            self.window = sg.Window("Sensor Data Display", self.layout)
            self.mqtt_client = self.setup_mqtt_client()
            self.data = {}
        except Exception as e:
            print(f"GUI initialization error: {e}")

    def setup_mqtt_client(self):
        """Set up the MQTT client and connect to the broker."""
        try:
            client = mqtt.Client()

            def on_connect(client, userdata, flags, rc):
                """Callback for when the client connects to the broker."""
                try:
                    print("Connected with result code " + str(rc))
                    # Subscribe to the topics where sensor data is published
                    client.subscribe("mytopic/iot/moisture/raw")
                    client.subscribe("mytopic/iot/moisture/percent")
                    client.subscribe("mytopic/iot/moisture/volts")
                except Exception as e:
                    print(f"Error in on_connect: {e}")

            def on_message(client, userdata, msg):
                """Callback for when a PUBLISH message is received from the server."""
                try:
                    topic = msg.topic.split("/")[-1]
                    self.data[topic] = msg.payload.decode()
                except Exception as e:
                    print(f"Error handling MQTT message: {e}")

            client.on_connect = on_connect
            client.on_message = on_message
            client.connect("test.mosquitto.org", 1883, 60)
            client.loop_start()
            return client
        except Exception as e:
            print(f"Failed to setup MQTT client: {e}")
            return None

    def get_sensor_data(self):
        """Fetch sensor data from the MQTT broker."""
        try:
            return self.data if hasattr(self, 'data') else None
        except Exception as e:
            print(f"Error getting sensor data: {e}")
            return None

    def run(self):
        """Run the event loop to update and display sensor data."""
        try:
            while True:
                event, values = self.window.read(timeout=1000)  # Update every second

                if event in (sg.WIN_CLOSED, "Exit"):
                    break
                
                # Update GUI with the latest data
                self.window["RAW"].update(self.data.get('raw', 'N/A'))
                self.window["PERCENT"].update(self.data.get('percent', 'N/A'))
                self.window["VOLTS"].update(self.data.get('volts', 'N/A'))
                
        except Exception as e:
            print(f"GUI runtime error: {e}")
        finally:
            self.window.close()

# Run the GUI
if __name__ == "__main__":
    try:
        display = SensorDataDisplay()
        display.run()
    except Exception as e:
        print(f"Error running SensorDataDisplay: {e}")