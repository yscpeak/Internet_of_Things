"""
Defines the Sensor class for moisture data readings from an ESP32 sensor.
"""

import machine
import network
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
        except Exception as e:
            print("sensor.py: Sensor:__init__: Error:", e)
            self.adc = None

    def moisture(self):
        """
        Returns moisture data as a dictionary with raw value, percent, voltage, and timestamp.
        """
        try:
            if self.adc:
                raw_value = self.adc.read()
                formatter = TimeFormatter()  # Create an instance of TimeFormatter
                # Adjust for Winnipeg CST time
                now = time.time()
                offset = -18000
                adjusted_time = time.localtime(now + offset)
                timestamp = formatter.format_time(adjusted_time)
                #timestamp = formatter.format_time(time.localtime())  # Use the format_time method from the TimeFormatter instance
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