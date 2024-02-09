import json

import customtkinter as ctk
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkSwitch
from customtkinter import CTkImage
from PIL import Image

def set_settings(settings: dict):
    with open('settings.json', 'w') as file:
        json.dump(settings, file, indent=4)

def get_settings() -> dict:
    with open('settings.json', 'r') as file:
        return json.load(file)

class RightMenuButton(CTkButton):
    # Static variable to keep track of the number of widgets created
    widget_count = 0
    
    def __init__(self, master, icon_name):
        # Initialize the parent class
        super().__init__(
            master=master,
            text='',
            width=40,
            height=40,
            # Load images for the button
            image=CTkImage(
                light_image=Image.open(f'icons\\{icon_name}.png'),
                dark_image=Image.open(f'icons\\{icon_name}.png')
            ),
            fg_color='transparent'
        )
        
    def place_by_index(self, flags=None) -> None:
        if flags == 'toend':
            self.place(x=5, y=255)
            return
        
        # Calculate the position of the button based on the index
        x = 5
        y = 5 + 40 * RightMenuButton.get_widget_count()
        
        # Place the button at the calculated position
        self.place(x=x, y=y)
        
        # Increment the widget count after placing the button
        RightMenuButton.widget_count += 1

    @classmethod
    def get_widget_count(cls) -> int:
        # Return the current count of widgets created
        return RightMenuButton.widget_count

class Main:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title('TrayModKit')
        self.app.geometry('600x300')
        self.app.resizable(0, 0)
        self.app.iconbitmap('icons\\main_icon.ico')
        
        self.right_menu_frame = CTkFrame(
            master=self.app,
            width=50,
            height=300,
            corner_radius=0
        )
        self.right_menu_frame.place(x=0, y=0)
        
        self.mini_apps_button = RightMenuButton(self.right_menu_frame, 'miniapps')
        self.mini_apps_button.place_by_index()
        
        self.themes_button = RightMenuButton(self.right_menu_frame, 'themes')
        self.themes_button.place_by_index(flags='toend')
        
        self.app.mainloop()
        
if __name__ == '__main__':
    Main()