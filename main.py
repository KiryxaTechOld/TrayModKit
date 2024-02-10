import time
import threading
import json

from PIL import Image
import customtkinter as ctk
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkImage

colors = {
    'border': ('#cacaca', '#303030'),
    'dark_frame': ('#cacaca', '#2b2b2b'),
    'transparent': 'transparent',
    'active_button': '#144870'
}


def set_settings(settings: dict):
    """Save settings to a JSON file."""
    with open('settings.json', 'w') as file:
        json.dump(settings, file, indent=4)


def get_settings() -> dict:
    """Load settings from a JSON file."""
    with open('settings.json', 'r') as file:
        return json.load(file)


class Switch(CTkButton):
    def __init__(self, master, mini_app_name) -> None:
        self.mini_app_name = mini_app_name
        self.is_active = get_settings()['mini_apps'][mini_app_name]['switch_active']
        
        super().__init__(
            master,
            text='',
            width=10,
            height=10,
            image=self.get_icon(),
            hover=False,
            fg_color=colors['transparent'],
            command=self.toggle
        )

    def toggle(self):
        self.is_active = not self.is_active
        self.configure(image=self.get_icon())
        
        settings = get_settings()
        settings['mini_apps'][self.mini_app_name]['switch_active'] = self.is_active
        set_settings(settings)
        
    def get_icon(self):
        icon_name = 'enabled' if self.is_active else 'disabled'
        return CTkImage(
            light_image=Image.open(f'icons\\light\\switch_{icon_name}.png'),
            dark_image=Image.open(f'icons\\dark\\switch_{icon_name}.png'),
            size=(40, 22)
        )


class RightMenuButton(CTkButton):
    """Custom button for the right menu."""
    instances = []
    widget_count = 0  # Static variable to keep track of the number of widgets created

    def __init__(self, master, icon_name, linked_page):
        """Initialize the button with an icon."""
        RightMenuButton.instances.append(self)
        
        super().__init__(
            master=master,
            width=40,
            height=40,
            fg_color=colors['transparent'],
            text='',
            image=self.load_icon(icon_name),
            command=lambda: self.active_self(linked_page)
        )

    def place_by_index(self, flags=None) -> None:
        """Place the button at a position calculated based on its index."""
        x = 5
        y = 5 + 40 * RightMenuButton.widget_count if flags != 'toend' else 255
        self.place(x=x, y=y)
        RightMenuButton.widget_count += 1  # Increment the widget count after placing the button

    @staticmethod
    def load_icon(icon_name):
        """Load the icon for the button."""
        return CTkImage(
            light_image=Image.open(f'icons\\{icon_name}.png'),
            dark_image=Image.open(f'icons\\{icon_name}.png')
        )
       
    @classmethod 
    def this_active_and_other_disable(cls, page_frame):
        PageFrame.set_page(page_frame)
        
    def set_color(self):
        for instance in RightMenuButton.instances:
            instance.configure(
                fg_color=colors['transparent']
            )
        
        self.configure(
            fg_color=colors['active_button']
        )
        
    def active_self(self, page_frame):
        self.set_color()
        RightMenuButton.this_active_and_other_disable(page_frame)


class MiniAppFrame(CTkFrame):
    """Custom frame for a mini application."""
    # Static variables to track the current coordinates
    column_heights = [10, 10]  # Heights of the columns
    widget_count = 0  # Counter for the widgets

    def __init__(self, master, title, height, icon_name):
        """Initialize the frame with a title, width, and height."""
        super().__init__(
            master=master,
            width=250,
            height=height,
            border_width=2,
            border_color=colors['border'],
            fg_color=colors['dark_frame'],
            corner_radius=7
        )
        
        self.height = height
        
        self.icon = CTkLabel(
            master=self,
            text='',
            image=CTkImage(
                light_image=Image.open(f'icons\\{icon_name}.png'),
                dark_image=Image.open(f'icons\\{icon_name}.png'),
                size=(15, 15)
            )
        )
        self.icon.place(x=10, y=4)
        
        self.title_label = CTkLabel(
            master=self,
            text=title,
            font=('Segoe UI Bold', 14)
        )
        self.title_label.place(x=30, y=5)
        
        self.switch = Switch(self, 'bin')
        self.switch.place(x=195, y=5)
        
    def set_switch_icon(self):
        is_active = get_settings()['mini_apps']['bin']['switch_active']
        if is_active:
            settings = get_settings()
            settings['mini_apps']['bin']['switch_active'] = False
            set_settings(settings)
            
            image_name = 'switch_disabled'
        else:
            settings = get_settings()
            settings['mini_apps']['bin']['switch_active'] = True
            set_settings(settings)
            
            image_name = 'switch_enabled'
        
        self.switch.configure(
            image=CTkImage(
                light_image=Image.open(f'icons\\light\\{image_name}.png'),
                dark_image=Image.open(f'icons\\dark\\{image_name}.png'),
                size=(40, 22)
            )
        )

    def place_stack_method(self):
        """Place the widget in a column based on the widget count."""
        height = self.height
        
        # Choose a column for placing the widget
        column_index = MiniAppFrame.widget_count % 2  # 0 for even, 1 for odd
        
        spacing = 0
        if column_index == 1:
            spacing = 10

        # Place the widget in the chosen column
        self.place(x=spacing + 250 * column_index, y=MiniAppFrame.column_heights[column_index])

        # Update the height of the column
        MiniAppFrame.column_heights[column_index] += height + 10  # 10 is the distance between widgets

        # Increment the widget counter
        MiniAppFrame.widget_count += 1


class PageFrame(CTkFrame):
    """Custom frame for a page."""
    instances = []

    def __init__(self, master, page_title):
        """Initialize the frame with a title."""
        super().__init__(
            master=master,
            width=550,
            height=300,
            fg_color=('#cfd2d4', '#202020'),
            corner_radius=0
        )

        self.page_title = CTkLabel(
            master=self,
            text=page_title,
            font=('Segoe UI Bold', 18)
        )
        self.page_title.place(x=10, y=10)

        PageFrame.instances.append(self)

    def show(self):
        """Show the frame."""
        self.place(x=50, y=0)

    def hide(self):
        """Hide the frame."""
        self.place_forget()

    @classmethod
    def set_page(cls, show_page):
        """Activate this page and hide all other pages."""
        for instance in PageFrame.instances:
            if instance == show_page:
                show_page.show()
            else:
                instance.place_forget()


class Main:
    """Main application class."""
    def __init__(self):
        """Initialize the application."""
        self.app = ctk.CTk()  # Create a CTk application
        self.app.title('TrayModKit')  # Set the title of the application
        self.app.geometry('600x300')  # Set the size of the application
        self.app.resizable(0, 0)  # Make the application non-resizable
        self.app.iconbitmap('icons\\main_icon.ico')  # Set the icon of the application

        ctk.set_appearance_mode('dark')  # Set the appearance mode of the application to light

        # Create a page for mini apps
        self.mini_apps_page = PageFrame(
            master=self.app,
            page_title='Mini-Apps'
        )
        self.mini_apps_page.show()  # Show the mini apps page
        
        self.themes_page = PageFrame(
            master=self.app,
            page_title='Themes'
        )

        # Create a frame for the right menu
        self.right_menu_frame = CTkFrame(
            master=self.app,
            width=50,
            height=300,
            fg_color=colors['dark_frame'],
            corner_radius=0
        )
        self.right_menu_frame.place(x=0, y=0)  # Place the right menu frame at the top left corner

        self.create_separated_line().place(x=49, y=0)  # Create a separated line and place it next to the right menu frame

        # Create buttons for the right menu
        self.mini_apps_button = RightMenuButton(self.right_menu_frame, 'miniapps', self.mini_apps_page)
        self.mini_apps_button.place_by_index()  # Place the mini apps button at the top of the right menu
        self.mini_apps_button.active_self(self.mini_apps_page)

        self.themes_button = RightMenuButton(self.right_menu_frame, 'themes', self.themes_page)
        self.themes_button.place_by_index(flags='toend')  # Place the themes button at the bottom of the right menu

        # Create a scrollable frame for the mini apps page
        self.scrollbar_frame = ctk.CTkScrollableFrame(
            master=self.mini_apps_page,
            fg_color='transparent',
            width=513,
            height=255
        )
        self.scrollbar_frame.place(x=10, y=36)  # Place the scrollable frame inside the mini apps page

        # Create an inner frame inside the scrollable frame
        self.inner_frame = CTkFrame(
            master=self.scrollbar_frame,
            width=520,
            height=1,
            fg_color='transparent'
        )
        self.inner_frame.pack(fill='both', expand=True)  # Make the inner frame fill the scrollable frame

        # Create mini app frames inside the inner frame
        self.create_mini_app_frame('MiniBin', 115, 'bin')
        
        self.set_inner_frame_height()  # Set the height of the inner frame

        self.app.mainloop()  # Start the application's main loop

    def create_mini_app_frame(self, title, height, icon_name):
        """Create a mini app frame and place it inside the inner frame."""
        mini_app_frame = MiniAppFrame(
            master=self.inner_frame,
            title=title,
            height=height,
            icon_name=icon_name
        )
        mini_app_frame.place_stack_method()  # Place the mini app frame inside the inner frame using the stack method

    def set_inner_frame_height(self):
        """Set the height of the inner frame based on the height of the mini app frames."""
        self.inner_frame.configure(height=max(MiniAppFrame.column_heights))  # Set the height of the inner frame to the maximum height of the mini app frames

    def create_separated_line(self) -> CTkFrame:
        """Create a separated line."""
        return CTkFrame(
            master=self.app,
            width=2,
            height=305,
            fg_color=colors['dark_frame'],
            corner_radius=0
        )  # Create a frame with a width of 2 and a height of 305 to be used as a separated line


if __name__ == '__main__':
    Main()
