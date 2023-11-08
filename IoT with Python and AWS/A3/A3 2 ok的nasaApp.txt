from requests import get
import json
from PIL import Image
from io import BytesIO
from menu import Menu

# Your NASA API key
API_KEY = "dQltGlSWwxd5BUmEbGGarsHq8mss4SkudOUE5JNf"

def display_photo(url):
    """Displays the photo found at url."""
    img_resp = get(url)
    img = Image.open(BytesIO(img_resp.content))
    img.show()
    img.close()

def fetch_data(url):
    """Fetches data from a given url."""
    try:
        response = get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None

def get_rover_photos(rover_name, date):
    """Fetches photos taken by a rover on a given date."""
    url_photos = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?earth_date={date}&api_key={API_KEY}"
    return fetch_data(url_photos)

def show_photo_menu(photos):
    """Shows a menu of photos for the user to choose from."""
    photo_menu = Menu()
    photo_menu.set_title("Mars Rover Photos")
    photo_menu.set_prompt("Choose a photo to view:")
    photo_options = [(f"Photo {i}", display_photo, [photo['img_src']]) for i, photo in enumerate(photos['photos'], start=1)]
    photo_menu.set_options(photo_options)
    photo_menu.open()

def rover_date_menu(rover_name):
    """Prompts for a date and shows the photos menu."""
    date = input(f"Enter a date (YYYY-MM-DD) for rover {rover_name}: ")
    camera = input(f"Enter a camera abbreviation (leave empty for all cameras): ")
    page = input(f"Enter page number (leave empty for first page): ")

    # Prepare the query parameters based on the user input
    params = {'earth_date': date, 'api_key': API_KEY}
    if camera:
        params['camera'] = camera
    if page:
        params['page'] = page

    # Fetch photos with the given parameters
    photos = get_rover_photos(rover_name, params)
    if photos['photos']:
        show_photo_menu(photos)
    else:
        print("No photos found for this date. Try another date.")

def main_menu():
    """Shows the main menu for choosing rovers and dates."""
    menu = Menu()
    menu.set_title("Mars Rover Explorer")
    menu.set_prompt("Choose an option:")
    rover_options = [
        ("Curiosity", lambda: rover_date_menu("curiosity")),
        ("Opportunity", lambda: rover_date_menu("opportunity")),
        ("Spirit", lambda: rover_date_menu("spirit")),
        ("Exit", Menu.CLOSE)
    ]
    menu.set_options(rover_options)
    menu.open()

if __name__ == "__main__":
    main_menu()
