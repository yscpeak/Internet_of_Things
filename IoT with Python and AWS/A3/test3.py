from requests import get
import json
from PIL import Image
from io import BytesIO
from menu import Menu

# Constants
API_KEY = 'dQltGlSWwxd5BUmEbGGarsHq8mss4SkudOUE5JNf'
BASE_URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/'

# Function to display a photo
def display_photo(url):
    """Displays the photo found at url."""
    img_resp = get(url)
    img = Image.open(BytesIO(img_resp.content))
    img.show()

# Function to get photos
def get_photos(rover_name, earth_date, camera='', page=1):
    camera_query = f"&camera={camera}" if camera else ""
    url = f"{BASE_URL}{rover_name}/photos?earth_date={earth_date}{camera_query}&page={page}&api_key={API_KEY}"
    return get(url).json()

# Function to select a photo
def select_photo(photos, rover_name, earth_date, page):
    photo_menu = Menu(title='Select a photo to view', prompt='Select an option:')

    for i, photo in enumerate(photos):
        photo_menu.add_option(f"Photo {i + 1}", lambda url=photo['img_src']: display_photo(url), kwargs={})

    # Pagination options
    if len(photos) == 25:  # Assuming API returns 25 photos per page
        photo_menu.add_option('Next Page', lambda: rover_date_menu(rover_name, earth_date, page + 1))
    if page > 1:
        photo_menu.add_option('Previous Page', lambda: rover_date_menu(rover_name, earth_date, page - 1))

    photo_menu.add_option('Return to Main Menu', main_menu)
    photo_menu.open()

# Function to choose date and get photos for a rover
def rover_date_menu(rover_name, earth_date='', page=1):
    if not earth_date:
        earth_date = input(f"Enter an Earth date (YYYY-MM-DD) to view {rover_name.capitalize()}'s photos: ")
    camera = input("Enter a camera abbreviation (leave empty for all cameras): ")
    page_input = input("Enter page number (leave empty for first page): ")
    page = int(page_input) if page_input else page

    photos = get_photos(rover_name, earth_date, camera, page)
    if photos['photos']:
        select_photo(photos['photos'], rover_name, earth_date, page)
    else:
        print(f"No photos found for {rover_name.capitalize()} on {earth_date}.")
        main_menu()

# Main menu function
def main_menu():
    main_menu = Menu(title='Mars Rover Photo Viewer', prompt='Select a Rover:')
    main_menu.add_option('Curiosity', lambda: rover_date_menu('curiosity'), kwargs={})
    main_menu.add_option('Opportunity', lambda: rover_date_menu('opportunity'), kwargs={})
    main_menu.add_option('Spirit', lambda: rover_date_menu('spirit'), kwargs={})
    main_menu.add_option('Exit', main_menu.close, kwargs={})  # Assuming .close is the correct method
    main_menu.open()

if __name__ == "__main__":
    main_menu()
