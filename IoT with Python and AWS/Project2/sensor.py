from machine import ADC, Pin
import time

class Sensor:
    """
    This class handles the interaction with an ADC sensor.
    """
    def __init__(self, pin):
        """
        Initialize the sensor.
        Sets up the ADC on the specified pin and 
        configures it for full range (0-3.3V) readings.
        """
        try:
            self.adc = ADC(Pin(pin))
            self.adc.atten(ADC.ATTN_11DB)  # Configure for the full range of 0-3.3V
        except Exception as e:
            print("sensor.py:Sensor:__init__:error:", e)

    def read_moisture(self):
        """
        Read and calculate the moisture level as a percentage.
        """
        try:
            value = self.adc.read()
            moisture_percent = (value / 4095) * 100
            return moisture_percent
        except Exception as e:
            print("sensor.py:Sensor:read_moisture:error:", e)
            return None

def get_sensor_data():
    """
    Retrieve and return the current moisture data from the sensor.
    """
    try:
        sensor = Sensor(36)
        moisture = sensor.read_moisture()
        return {
            "moisture": moisture
        }
    except Exception as e:
        print("sensor.py:get_sensor_data:error:", e)
        return {"moisture": None}

if __name__ == "__main__":
    """
    Main execution block for direct script run.
    """
    try:
        while True:
            try:
                data = get_sensor_data()
                print("Moisture Level:", data["moisture"], "%")
                time.sleep(10)  # Read sensor data every 10 seconds
            except Exception as e:
                print("sensor.py:main:while_loop:error:", e)
    except Exception as e:
        print("sensor.py:main:error:", e)
