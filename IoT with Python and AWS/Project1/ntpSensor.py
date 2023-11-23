"""
Defines the Sensor class for moisture data readings from an ESP32 sensor.
"""

import machine
from ntptime import settime
import time
from time_formatter import TimeFormatter  # Import the TimeFormatter class

class Sensor:
    """Handles ADC readings from a moisture sensor."""

    def __init__(self, pin):
        """Initializes the ADC for the sensor on the specified pin."""
        try:
            self.adc = machine.ADC(machine.Pin(pin))
            self.adc.atten(machine.ADC.ATTN_11DB)
            self.set_ntp_time()  # Set the NTP time when initializing the sensor
            self.display_time()  # Display the set time
        except Exception as e:
            print("sensor.py: Sensor:__init__: Error:", e)
            self.adc = None

    def set_ntp_time(self):
        """Sets the device's time using NTP."""
        try:
            settime()  # Synchronize time with NTP server
        except Exception as e:
            print("Error setting NTP time:", e)
    
    def display_time(self):
        """Displays the current time on the terminal."""
        try:
            current_time = time.localtime()
            formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*current_time[:6])
            print("Current Time:", formatted_time)
        except Exception as e:
            print("Error displaying time:", e)

    def moisture(self):
        """
        Returns moisture data as a dictionary with raw value, percent, voltage, and timestamp.
        """
        try:
            if self.adc:
                raw_value = self.adc.read()
                formatter = TimeFormatter()  # Create an instance of TimeFormatter
                # Use the format_time method from the TimeFormatter instance
                timestamp = formatter.format_time(time.localtime())  
                return {
                    'raw': raw_value,
                    'percent': 100 * raw_value / 4095,
                    'volts': 3.3 * raw_value / 4095,
                    'timestamp': timestamp
                }
            else:
                print("ADC not initialized.")
                return None
        except Exception as e:
            print("sensor.py: Sensor:moisture: Error:", e)
            return None

sensor = Sensor(pin=36)