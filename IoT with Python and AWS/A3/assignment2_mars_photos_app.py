from requests import get
from PIL import Image
from io import BytesIO
from menu import Menu
import re

API_KEY = "eyTh79JpYExIl7l3uwC6A5OaBbwHc7CY6IM79DVr"
url_rovers = f"https://api.nasa.gov/mars-photos/api/v1/rovers?api_key={API_KEY}"

class MarsPhotoApp:

    def __init__(self):
        self.selected_rover = None
        self.selected_date = None
        self.photo_urls = []
        self.current_page = 0

        self.main_menu = Menu(
            title="Main Menu",
            message="Choose one of the available rovers(try Curiosity):",
            auto_clear=False
        )
        self.main_menu.set_prompt(">")

        self.photos_menu = Menu(
            title="",
            message="Choose a photo or 'Return to Main Menu':",
            auto_clear=False
        )
        self.photos_menu.set_prompt(">")

        rover_options = self.get_rover_options()
        self.main_menu.set_options(rover_options)

    def get_rovers(self):
        response = get(url_rovers)
        rovers_data = response.json()
        return rovers_data.get("rovers", [])

    def get_rover_options(self):
        rover_options = []
        for rover in self.get_rovers():
            rover_name = rover["name"]
            option = (rover_name, self.select_rover, {"rover_name": rover_name})
            rover_options.append(option)
        rover_options.append(("Exit", self.exit_program))
        return rover_options
    
    def exit_program(self):
        print("Exiting the program.")
        exit()  # exit the program
    
    def select_rover(self, rover_name):
        self.selected_rover = rover_name
        #validate the date
        regex = r"^\d{4}-\d{2}-\d{2}$"
        while True:
            self.selected_date = input("Please enter a date (YYYY-MM-DD) or 'Exit' to go back to the Main Menu: ")
            if self.selected_date.lower() == "exit":
                self.photos_menu.close()
                self.main_menu.open()   
            else:
                #check if the date is valid
                if re.match(regex, self.selected_date):
                    self.get_photo_urls()
                    break
                
            

    def get_photo_urls(self):
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{self.selected_rover}/photos?earth_date={self.selected_date}&api_key={API_KEY}"
        response = get(url)
        photos_data = response.json()
        self.photo_urls = [photo["img_src"] for photo in photos_data.get("photos", [])]
        self.current_page = 0
        self.display_photos_menu()

    def display_photos_menu(self):
        self.photos_menu.set_title(f"{self.selected_rover} Photos Menu")
        self.photos_menu.set_message("Choose a photo or 'Return to Main Menu':")
        self.photos_menu.set_prompt(">")
        
        #start_idx is the index of the first photo in the current page
        #end_idx is the index of the last photo in the current page
        start_idx = self.current_page * 10
        end_idx = (self.current_page + 1) * 10
        #self.photo_urls[:] is a list of the 10 photos in the current page
        current_page_photos = self.photo_urls[start_idx:end_idx]
        self.update_photo_options(current_page_photos)
        
        while True:
            #user_choice will be assigned the value of the option that the user selects from the opened menu
            user_choice = self.photos_menu.open()
            #check if the user_choice is callable, if it is, call it，otherwise, check if the user_choice is "Return to Main Menu", if it is, close the photos_menu and open the main_menu
            if callable(user_choice):
                user_choice()
            elif user_choice == "Return to Main Menu":
                self.main_menu.open()
                break

    def update_photo_options(self, photo_urls):
        photo_options = []
        for i, photo_url in enumerate(photo_urls, 1):
            photo_option = (f"{photo_url}", self.display_photo, {"url": photo_url})
            photo_options.append(photo_option)

        if self.current_page > 0:
            photo_options.append(("Previous Page", self.handle_previous_page))
        if len(photo_urls) >= 10:
            photo_options.append(("Next Page", self.handle_next_page))

        photo_options.append(("Return to Main Menu", self.main_menu.open))

        self.photos_menu.set_options(photo_options)

    def handle_next_page(self):
        #check if the current page is the last page, if not, update the photo options with the next page photos
        if self.current_page < len(self.photo_urls) // 10:
            self.current_page += 1
            start_idx = self.current_page * 10
            end_idx = (self.current_page + 1) * 10
            next_page_photos = self.photo_urls[start_idx:end_idx]
            self.update_photo_options(next_page_photos)

    def handle_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            start_idx = self.current_page * 10
            end_idx = (self.current_page + 1) * 10
            previous_page_photos = self.photo_urls[start_idx:end_idx]
            self.update_photo_options(previous_page_photos)

    def display_photo(self, url):
        response = get(url)
        img = Image.open(BytesIO(response.content))
        img.show()
        img.close()

    def run(self):
        #open the main menu,app is an instance of MarsPhotoApp
        app = MarsPhotoApp()
        app.main_menu.open()
        
  

if __name__ == "__main__":
    MarsPhotoApp().run()