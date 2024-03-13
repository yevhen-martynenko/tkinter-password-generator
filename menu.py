import ttkbootstrap as ttk

import tkinter as tk 
import webbrowser
from random import choice
import json


class Menu(tk.Menu):
    def __init__(self, master, settings_frame):
        # setup
        super().__init__(master=master)
        self.config(tearoff=False)

        # show the settings window
        self.settings_frame = settings_frame
        self.add_command(label='Settings', command=self.settings_frame.animate_settings_frame)


        # create a menu with a settings
        settings_menu = tk.Menu(self, tearoff=False)

        # create a checkbutton to switch the program to "Above all other windows" mode
        self.topmost_check_var = tk.BooleanVar(value=False)
        settings_menu.add_checkbutton(label='Top', onvalue=True, offvalue=False, variable=self.topmost_check_var)
        self.topmost_check_var.trace('w', lambda *args: master.attributes('-topmost', self.topmost_check_var.get()))

        # create a checkbutton to show/hide title bar
        self.title_bar_var = tk.BooleanVar(value=False)
        settings_menu.add_checkbutton(label='Title bar', onvalue=False, offvalue=True, variable=self.title_bar_var, 
                                      command=lambda: self.title_bar(master))
        
        # create a checkbutton to stay in tray
        self.stay_tray_var = tk.BooleanVar(value=True)
        settings_menu.add_checkbutton(label='Stay in Tray', onvalue=True, offvalue=False, variable=self.stay_tray_var)
        
        
        self.add_cascade(label='Advanced Settings', menu=settings_menu)


        # create a menu with a themes
        self.theme_name = tk.StringVar(value='cosmo')
        themes_menu = tk.Menu(self, tearoff=False)

        # create lists of themes
        light_themes = ['cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean']
        dark_themes = ['solar', 'superhero', 'darkly', 'cyborg', 'vapor', 'test']

        # create lists of user themes
        self.user_themes = []
        try: 
            self.get_user_themes() 
        except Exception: 
            pass

        # create lists of all themes
        themes = light_themes.copy() + dark_themes.copy() + self.user_themes.copy()


        # create a submenu with a light themes
        light_themes_menu = tk.Menu(self, tearoff=False)
        for light_theme in light_themes:
            light_themes_menu.add_command(label=light_theme, command=lambda theme=light_theme: self.change_theme(theme))
        themes_menu.add_cascade(label='Light', menu=light_themes_menu)

        # create a submenu with a dark themes
        dark_themes_menu = tk.Menu(self, tearoff=False)

        for dark_theme in dark_themes:
            dark_themes_menu.add_command(label=dark_theme, command=lambda theme=dark_theme: self.change_theme(theme))
        themes_menu.add_cascade(label='Dark', menu=dark_themes_menu)

        # create a submenu with a user themes
        self.user_themes_menu = tk.Menu(self, tearoff=False)

        for user_theme in self.user_themes:
            self.user_themes_menu.add_command(label=user_theme, command=lambda theme=user_theme: self.change_theme(theme))
        themes_menu.add_cascade(label='User', menu=self.user_themes_menu)


        themes_menu.add_separator()
    
        # chooses a random theme
        themes_menu.add_command(label="Random Theme", command=lambda: self.change_theme(choice(themes)))

        self.add_cascade(label='Themes', menu=themes_menu)


        # create a help menu
        help_menu = ttk.Menu(self, tearoff=False)

        help_menu.add_command(label='LinkedIn', command=lambda: webbrowser.open_new(r"https://www.linkedin.com/in/yevhen-martynenko-9389062b5/"))
        help_menu.add_separator()
        help_menu.add_command(label='Github', command=lambda: webbrowser.open_new(r"https://github.com/yevhen-martynenko")) 


        self.add_cascade(label='Help', menu=help_menu)


        self.add_separator()

        # create a button to close the program
        self.settings_frame = settings_frame
        self.add_command(label='Close', command=lambda: self.master.hide_window(True))


    def change_theme(self, theme_name):
        # transfer the data and run the "setting the theme" method
        self.theme_name.set(theme_name)
        self.master.set_style(self.theme_name.get())

    
    def title_bar(self,master): 
        # titlebar settings
        master.overrideredirect(self.title_bar_var.get())

        if self.title_bar_var.get():
            master.moving_label.configure(style='TitleBarInactive.TLabel')
        elif not self.title_bar_var.get():
            master.moving_label.configure(style='TitleBarActive.TLabel')
    

    def get_user_themes(self):
        # get user theme names
        self.master.download_users_styles()
        try:
            with open('styles/user_styles.json', 'r') as file:
                data = json.load(file)
                themes_data = data.get("themes", [])

            for theme_data in themes_data:
                keys = list(theme_data.keys())
                self.user_themes.append(keys[0])
            
            self.add_user_theme(keys[0])
        except Exception:
            pass

    def add_user_theme(self, user_theme):
        # add user theme after creation
        self.user_themes_menu.add_command(label=user_theme, command=lambda theme=user_theme: self.change_theme(theme))
