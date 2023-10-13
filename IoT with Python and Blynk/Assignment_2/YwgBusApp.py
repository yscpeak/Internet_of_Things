'''
Internet of Things with Python Blynk AWS
Assignment2
Yi Siang Chang
2023-09-11
'''

from requests import get
from dateutil.parser import parse
from colorama import init, Fore, Back, Style

init(autoreset=True) # Initialize colorama with autoreset

# Function to get arrival times for a specific bus stop
def get_arrival_times(stop_id):
    url = f"https://api.winnipegtransit.com/v3/stops/{stop_id}/schedule.json?api-key={API_KEY}"
    try:
        data = get(url).json()

        if 'stop-schedule' in data and 'stop' in data['stop-schedule']:
            if 'route-schedules' in data['stop-schedule']:
                return data['stop-schedule']['route-schedules']
            else:
                print("Debug: 'route-schedules' key missing. Raw data:", data)
                return []
        else:
            print("Debug: Unexpected data structure. Raw data:", data)
            return []

    except Exception as e:
        print(f"Error fetching arrival times: {e}")
        return []

# Convert timestamp to formatted time
def format_time(timestamp):
    return parse(timestamp).strftime("%H:%M:%S")

API_KEY = 'OB8IwqWHx00vYV5UEq5S'

# Setup
lat = 49.895  # GPS latitude of location
lon = -97.138 # GPS longitude of location
distance = 100  # radius in meters to search around GPS coordinates

# URL construction & request
url_stops = f"https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={API_KEY}"

try:
    resp_stops = get(url_stops).json()

    # Create a dictionary of stop names and their stop numbers
    stops_dict = {}
    for stop in resp_stops['stops']:
        stop_name = stop['name']
        stop_number = stop['key']
        stops_dict[stop_number] = stop_name
        print(f"{stop_name} - Stop number: {stop_number}")

    # Choose a bus stop
    while True:
        chosen_stop_number = int(input("\nEnter the stop number: "))
        if chosen_stop_number in stops_dict:
            break
        print("Invalid stop number, please enter a valid stop number.")

    # Fetch and display arrival times
    arrival_times = get_arrival_times(chosen_stop_number)
    for route in arrival_times:
        print(f"\nRoute {route['route']['key']} - {route['route']['name']}:")
        for schedule in route['scheduled-stops']:
            scheduled_time = format_time(schedule['times']['arrival']['scheduled'])
            estimated_time = format_time(schedule['times']['arrival']['estimated'])

            if scheduled_time < estimated_time:
                color = Fore.RED  # Late
            elif scheduled_time > estimated_time:
                color = Fore.BLUE  # Early
            else:
                color = Fore.GREEN  # On time

            print(f"  {color}Scheduled: {scheduled_time} - Estimated: {estimated_time}")

except Exception as e:
    print(f"Error: {e}")