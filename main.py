import ttkbootstrap as ttk
from ttkbootstrap import Style
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk

import tkinter as tk
import _tkinter
import json

from frames import ConfigurationFrame, OutputFrame, SettingsFrame
from menu import Menu
from styles.styles_configure import configure_styles


password = ''


class App(tk.Tk):
    def __init__(self, title, size, min_size):
        """
        Create a program window with the specified title, size, and minimum size.

        Args:
            title (str): The title of the program window.
            size (tuple of int): A tuple containing the width and height of the program window.
            min_size (tuple of int): A tuple containing the minimum width and height of the program window.
        
        Example: 
            app = App("My Program", (800, 600), (400, 300))
        """

        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(min_size[0], min_size[1])
        self.resizable(False, False)
        self.overrideredirect(True)
        self.protocol('WM_DELETE_WINDOW', func=lambda: self.hide_window(False))
        # set icon image
        try:
            self.iconbitmap('logo.ico')
        except _tkinter.TclError:
            im = Image.open('logo.ico')
            icon = ImageTk.PhotoImage(im)
            self.wm_iconphoto(True, icon)

        self.password_var = tk.StringVar(value=password)

        # moving window without title bar
        self.moving_label = ttk.Label(self)
        self.moving_label.configure(style='TitleBarActive.TLabel')
        self.moving_label.pack(expand=True, fill='both')

        self.moving_label.bind("<ButtonPress-1>", self.start_drag)
        self.moving_label.bind("<B1-Motion>", self.move_window)
        self.moving_label.bind("<Enter>", self.change_cursor)
        self.moving_label.bind("<Leave>", self.return_cursor)

        # widgets
        self.output = OutputFrame(self, self.password_var)
        self.configuration = ConfigurationFrame(self, self.output)
        self.settings = SettingsFrame(self, 0, 1)

        # menu
        self.menu = Menu(self, self.settings)

        # keyboard shortcuts
        self.bind_all('<Escape>',lambda event: self.quit())

        # styles
        self.style = Style()
        # download custom styles
        try:
            styles_file = 'styles/styles.json'
            self.style.load_user_themes(styles_file)
            configure_styles(self.style)
        except json.decoder.JSONDecodeError:
            pass

        # download users styles
        self.download_users_styles()
        
        # load user settings data
        self.load_data()

        self.set_style(self.theme_name)
        self.menu.topmost_check_var.set(self.top)
        self.menu.title_bar_var.set(self.title_bar)
        self.menu.title_bar(self)
        self.menu.stay_tray_var.set(self.stay_in_tray)

        self.settings.program_settings.opacity_var.set(self.opacity)
        self.settings.program_settings.change_opacity(self.settings.program_settings, 0)

        # run
        self.config(menu=self.menu)
        self.mainloop()
    

    def set_style(self, theme_name):
        # setting the theme
        self.theme_name = theme_name
        self.style.theme_use(self.theme_name)
    
    def download_users_styles(self):
        user_styles_file = 'styles/user_styles.json'
        try:
            self.style.load_user_themes(user_styles_file)
        except json.decoder.JSONDecodeError:
            pass


    def start_drag(self, event):
        # get mouse coordinates
        self._x, self._y = event.x, event.y

    def move_window(self, event):
        x, y = event.x, event.y 
        self.geometry(f"+{self.winfo_x() + (x - self._x)}+{self.winfo_y() + (y - self._y)}")
    

    def change_cursor(self, event):
        # change the cursor when hovering over the button
        self.moving_label.config(cursor='fleur') 

    def return_cursor(self, event):
        # return the standard cursor when the button is released
        self.moving_label.config(cursor='')

    
    # stay in system tray
    def hide_window(self, is_instant_closure):

        image=Image.open("logo.ico")
        menu=(item('Show', self.show_window, default=True), item('Quit', self.quit_window))
        icon=pystray.Icon(name="app", icon=image, title="Password Generator", menu=menu)

        if is_instant_closure:
            self.quit_window(icon, menu)
        elif not is_instant_closure:
            if self.menu.stay_tray_var.get():
                self.withdraw()
                icon.run()
            elif not self.menu.stay_tray_var.get():
                self.quit_window(icon, menu)
         
    def quit_window(self, icon, item):
        self.save_data()
        icon.stop()
        self.destroy()

    def show_window(self, icon, item):
        icon.stop()
        self.after(0, self.deiconify)


    # save/download data from json file
    def save_data(self):
        # save the settings data to a json file
        data = {}
        theme_name = self.theme_name
        top = self.menu.topmost_check_var.get()
        title_bar = self.menu.title_bar_var.get()
        stay_in_tray = self.menu.stay_tray_var.get()
        opacity = self.settings.program_settings.opacity_var.get()

        data['theme_name'] = theme_name
        data['top'] = top
        data['title_bar'] = title_bar
        data['stay_in_tray'] = stay_in_tray
        data['opacity'] = opacity

        print(data)
        with open('save.json', 'w') as file:
            json.dump(data, file)

    def load_data(self):
        # download settings data from json file
        try:
            with open('save.json', 'r') as file:
                data = json.load(file)
                self.theme_name = data["theme_name"]
                self.top = data["top"]
                self.title_bar = data["title_bar"]
                self.stay_in_tray = data["stay_in_tray"]
                self.opacity = data["opacity"]
        except Exception:
            self.theme_name = 'cosmo'
            self.top = False
            self.title_bar = False
            self.stay_in_tray = True
            self.opacity = 100

    def reset_data(self):
        with open('save.json', 'w') as file:
            json.dump({}, file)
        self.hide_window(False)


app = App(title='password generator'.upper(), size=(700, 400), min_size=(700, 400))
