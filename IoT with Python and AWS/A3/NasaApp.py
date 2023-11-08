import re
from requests import get
from PIL import Image
from io import BytesIO
from menu import Menu

# Constants
API_KEY = 'dQltGlSWwxd5BUmEbGGarsHq8mss4SkudOUE5JNf'
NASA_API_BASE_URL = 'https://api.nasa.gov'
ROVERS_ENDPOINT = f"{NASA_API_BASE_URL}/mars-photos/api/v1/rovers"


class NasaApp:
    def __init__(self):
        # Initialize instance variables
        self.selected_rover = None
        self.selected_date = None
        self.photo_urls = []
        self.current_page = 0

        # Initialize menus
        self.main_menu = Menu(title="Main Menu", message="Please select one:", auto_clear=False)
        self.photos_menu = Menu(title="", message="Select a photo or 'Return to the Main Menu':", auto_clear=False)

        # Set menu prompts
        self.main_menu.set_prompt(">")
        self.photos_menu.set_prompt(">")

        # Populate rover options
        rover_options = self.get_rover_options()
        self.main_menu.set_options(rover_options)

    # Fetch rover data from NASA API
    def get_rovers(self):
        response = get(f"{ROVERS_ENDPOINT}?api_key={API_KEY}")
        rovers_data = response.json()
        return rovers_data.get("rovers", [])

    # Generate rover options for the main menu
    def get_rover_options(self):
        rover_options = [(rover["name"], self.select_rover, {"rover_name": rover["name"]}) for rover in
                         self.get_rovers()]
        rover_options.append(("Exit", self.exit_program))
        return rover_options

    # Exit the program
    def exit_program(self):
        print("Successfully exited. PLZ COME BACK SOON!")
        exit()

    # Select a rover and enter a date
    def select_rover(self, rover_name):
        self.selected_rover = rover_name
        regex = r"^\d{4}-\d{2}-\d{2}$"
        while True:
            self.selected_date = input("Please enter a date (eg. 2015-05-30) or input 'exit' to return to the Main Menu: ")
            if self.selected_date.lower() == "exit":
                self.photos_menu.close()
                self.main_menu.open()
            else:
                if re.match(regex, self.selected_date):
                    self.get_photo_urls()
                    break

    # Fetch photo URLs for the selected rover and date
    def get_photo_urls(self):
        url = f"{NASA_API_BASE_URL}/mars-photos/api/v1/rovers/{self.selected_rover}/photos"
        params = {"earth_date": self.selected_date, "api_key": API_KEY}
        response = get(url, params=params)
        photos_data = response.json()
        self.photo_urls = [photo["img_src"] for photo in photos_data.get("photos", [])]
        self.current_page = 0
        self.display_photos_menu()

    # Display the menu for selecting photos
    def display_photos_menu(self):
        self.photos_menu.set_title(f"{self.selected_rover} Photos Menu")
        self.photos_menu.set_message("Select a Photo or 'Return to the Main Menu':")
        self.photos_menu.set_prompt(">")

        start_idx = self.current_page * 10
        end_idx = (self.current_page + 1) * 10
        current_page_photos = self.photo_urls[start_idx:end_idx]
        self.update_photo_options(current_page_photos)

        while True:
            user_choice = self.photos_menu.open()

            if callable(user_choice):
                user_choice()
            elif user_choice == "Return to the Main Menu":
                self.main_menu.open()
                break

    # Update photo options based on the current page
    def update_photo_options(self, photo_urls):
        photo_options = [(f"{photo_url}", self.display_photo, {"url": photo_url}) for photo_url in photo_urls]

        if self.current_page > 0:
            photo_options.append(("Previous Page", self.previous_page))
        if len(photo_urls) >= 10:
            photo_options.append(("Next Page", self.next_page))

        photo_options.append(("Return to the Main Menu", self.main_menu.open))
        self.photos_menu.set_options(photo_options)

    # Go to the next page of photos
    def next_page(self):
        if self.current_page < len(self.photo_urls) // 10:
            self.current_page += 1
            start_idx = self.current_page * 10
            end_idx = (self.current_page + 1) * 10
            next_page_photos = self.photo_urls[start_idx:end_idx]
            self.update_photo_options(next_page_photos)

    # Go to the previous page of photos
    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            start_idx = self.current_page * 10
            end_idx = (self.current_page + 1) * 10
            previous_page_photos = self.photo_urls[start_idx:end_idx]
            self.update_photo_options(previous_page_photos)

    # Display a selected photo
    def display_photo(self, url):
        response = get(url)
        img = Image.open(BytesIO(response.content))
        img.show()
        img.close()

    # Run the program
    def run(self):
        self.main_menu.open()

# Entry point of the program
if __name__ == "__main__":
    app = NasaApp()
    app.run()
