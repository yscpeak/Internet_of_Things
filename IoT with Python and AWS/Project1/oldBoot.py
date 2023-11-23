"""
Executed on ESP32 boot-up to handle WiFi connection and time sync using NTP.
"""

import network
import ntptime
from ntptime import settime
import time
from time_formatter import TimeFormatter  # Import the TimeFormatter class

try:
    SSID = 'iPhone'
    PASSWORD = '11281128'
except Exception as e:
    print("boot.py:SSID/PASSWORD initialization:Error:", e)

def connect_wifi():
    """Establishes WiFi connection."""
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(SSID, PASSWORD)

        max_attempts = 10
        attempts = 0
        while not wlan.isconnected() and attempts < max_attempts:
            time.sleep(1)
            attempts += 1

        if wlan.isconnected():
            print("Connected. IP address:", wlan.ifconfig()[0])
        else:
            print("Failed to connect to WiFi after several attempts.")
            return False

        return True
    except Exception as e:
        print("boot.py: connect_wifi: Error:", e)
        return False

# def format_time(t):
#     """Formats time in YYYY-MM-DD HH:MM:SS format."""
#     try:
#         year, month, day, hour, minute, second, _, _ = t
#         return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second)
#     except Exception as e:
#         print("Error in formatting time:", e)
#         return None

def set_time_from_ntp():
    """Sets system time using NTP."""
    try:
        ntptime.host = 'pool.ntp.org'
        ntptime.settime()
        formatter = TimeFormatter()  # Create an instance of TimeFormatter
        # Adjust for Winnipeg CST time (winter)
        now = time.time()
        adjusted_time = time.localtime(now - 18000)  # 5 hours * 3600 seconds/hour
        #formatted_time = time.format_time('%Y-%m-%d %H:%M:%S', adjusted_time)
        formatted_time = formatter.format_time(adjusted_time)  # Use the format_time method
        print("Winnipeg time (CST):", formatted_time)
    except Exception as e:
        print("boot.py: set_time_from_ntp: Error:", e)

try:
    connect_wifi()
except Exception as e:
    print("boot.py: connect_wifi call: Error:", e)

try:
    set_time_from_ntp()
except Exception as e:
    print("boot.py: set_time_from_ntp call: Error:", e)
