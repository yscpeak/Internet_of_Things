from requests import get
import json
from PIL import Image
from io import BytesIO
from menu import Menu

API_KEY = "dQltGlSWwxd5BUmEbGGarsHq8mss4SkudOUE5JNf"

def display_photo(url):
    """Displays the photo found at url."""
    try:
        img_resp = get(url)
        img_resp.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        img = Image.open(BytesIO(img_resp.content))
        img.show()
        # Consider adding a delay here if the image closes immediately
    except Exception as e:
        print(f"An error occurred: {e}")

def fetch_data(url):
    """Fetches data from a given url."""
    try:
        response = get(url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_rover_photos(rover_name, date):
    """Fetches photos taken by a rover on a given date."""
    url_photos = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?earth_date={date}&api_key={API_KEY}"
    return fetch_data(url_photos)


def show_photo_menu(photos, start_index=0):
    """Shows a menu of photos for the user to choose from."""
    max_index = len(photos['photos'])
    end_index = min(start_index + 10, max_index)
    photo_slice = photos['photos'][start_index:end_index]

    photo_menu = Menu("Mars Rover Photos", "Choose a photo to view:")

    for i, photo in enumerate(photo_slice, start=1):
        photo_menu.add_option(f"Photo {start_index + i}", lambda url=photo['img_src']: display_photo(url))

    if start_index + 10 < max_index:
        photo_menu.add_option("Next", lambda: show_photo_menu(photos, start_index=start_index + 10))
    if start_index > 0:
        photo_menu.add_option("Back", lambda: show_photo_menu(photos, start_index=start_index - 10))

    photo_menu.add_option("Return to Main Menu", main_menu)
    photo_menu.show()

def rover_date_menu(rover_name):
    """Prompts for a date and shows the photos menu."""
    date = input(f"Enter a date (YYYY-MM-DD) for rover {rover_name}: ")
    photos = get_rover_photos(rover_name, date)
    if photos and 'photos' in photos:  # Check that photos is not None and has the 'photos' key
        show_photo_menu(photos)
    else:
        print("No photos found for this date or an error occurred. Try another date.")
        main_menu()


def main_menu():
    """Shows the main menu for choosing rovers and dates."""
    main_menu = Menu("Mars Rover Explorer", "Choose an option:")

    # Add options to the menu
    main_menu.add_option("Curiosity", rover_date_menu, kwargs={'rover_name': 'curiosity'})
    main_menu.add_option("Opportunity", rover_date_menu, kwargs={'rover_name': 'opportunity'})
    main_menu.add_option("Spirit", rover_date_menu, kwargs={'rover_name': 'spirit'})
    main_menu.add_option("Exit", exit)

    # Show the menu
    main_menu.open()


# if __name__ == '__main__':
#     main_menu()
