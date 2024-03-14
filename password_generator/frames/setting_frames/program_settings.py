import ttkbootstrap as ttk

import tkinter as tk 
from tkinter import messagebox
import json


class ProgramSettingsTab(ttk.Frame):
    def __init__(self, master):
        # setup
        super().__init__(master=master)

        # create widgets
        self.create_widgets()

        # place widgets
        self.place_widgets()

        # create events
        self.create_events()
    
    def create_widgets(self):
        # create labels
        self.title_label = ttk.Label(self, text='Settings', anchor='center', font=('Helvetica', 20, 'bold'))

        self.opacity_label = ttk.Label(self, text='Opacity:', anchor='center', font=('Helvetica', 12, 'normal'))

        # create an opacity scale with its variables
        self.opacity_min = 10
        self.opacity_max = 100
        self.opacity_var = tk.IntVar(value=100)
        self.opacity_scale = ttk.Scale(self, from_=self.opacity_min, to=self.opacity_max, length=self.winfo_width(), orient='horizontal', variable=self.opacity_var, command=lambda value: self.change_opacity(value))

        # create a combobox of items to delete
        self.combobox_label = ttk.Label(self, text='Select a theme to delete:', anchor='center', font=('Helvetica', 12, 'normal'))

        self.themes = []
        self.theme_to_delete = tk.StringVar()
        self.themes_combobox = ttk.Combobox(self, textvariable=self.theme_to_delete)

        self.get_theme_list()

        self.delete_button = ttk.Button(self, text='Delete', command=self.delete_theme)

        # create reset button
        self.reset_button = ttk.Button(self, text='Reset', command=self.reset_settings)

    def place_widgets(self):
        # create grid system
        self.columnconfigure((0,1,2), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3,4,5), weight=1, uniform='a')

        # place main title
        self.title_label.grid(row=0, column=0, columnspan=3, sticky='nesw')

        # place widgets to change opacity
        self.opacity_label.grid(row=1, column=0, sticky='nesw')
        self.opacity_scale.grid(row=1, column=1, columnspan=2, sticky='nesw', padx=20)

        # place widgets to delete the theme
        self.combobox_label.grid(row=2, column=0, sticky='nesw')
        self.themes_combobox.grid(row=2, column=1, sticky='nesw', pady=15, padx=5)
        self.delete_button.grid(row=2, column=2, sticky='nesw', pady=15, padx=20)

        # place reset button
        self.reset_button.grid(row=5, column=1, sticky='nesw', pady=10)

    def create_events(self):
        # event for opacity_scale
        self.opacity_scale.bind('<MouseWheel>', self.on_scale_scroll)
        self.opacity_scale.bind('<Button-4>', self.on_scale_scroll)
        self.opacity_scale.bind('<Button-5>', self.on_scale_scroll)

        # hover events
        self.opacity_scale.bind("<Enter>", lambda event, widget=self.opacity_scale: self.change_cursor(event, widget))
        self.opacity_scale.bind("<Leave>", lambda event, widget=self.opacity_scale: self.return_cursor(event, widget))

        self.themes_combobox.bind("<Enter>", lambda event, widget=self.themes_combobox: self.change_cursor(event, widget))
        self.themes_combobox.bind("<Leave>", lambda event, widget=self.themes_combobox: self.return_cursor(event, widget))
        self.delete_button.bind("<Enter>", lambda event, widget=self.delete_button: self.change_cursor(event, widget))
        self.delete_button.bind("<Leave>", lambda event, widget=self.delete_button: self.return_cursor(event, widget))

        self.reset_button.bind("<Enter>", lambda event, widget=self.reset_button: self.change_cursor(event, widget))
        self.reset_button.bind("<Leave>", lambda event, widget=self.reset_button: self.return_cursor(event, widget))
    

    def change_opacity(self, *args):
        opacity = float(self.opacity_var.get() / 100)
        self.master.master.attributes('-alpha', opacity)


    def get_theme_list(self):
        # get a list of theme names from a json file
        try:
            with open('styles/user_styles.json', 'r') as file:
                data = json.load(file)
                self.themes_data = data.get("themes", [])
        except Exception:
            self.themes_data = []
        else:
            if self.themes_data != []:
                for index in range(len(self.themes_data)):
                    if list(self.themes_data[index])[0] not in self.themes:
                        self.themes.append(list(self.themes_data[index])[0])
                
                self.theme_to_delete.set(value=self.themes[0])
                self.themes_combobox.config(values=self.themes)
            else:
                self.theme_to_delete.set(value=self.themes)
                self.themes_combobox.config(values=self.themes)

    def delete_theme(self):
        # method to delete the selected theme

        theme_to_delete = self.theme_to_delete.get()

        if theme_to_delete:
            answer = messagebox.askokcancel(title='Delete theme', message=f'Delete this theme: {theme_to_delete}?')

            if answer:
                for index in range(len(self.themes_data)):
                    if theme_to_delete == list(self.themes_data[index])[0]:
                        del self.themes_data[index]
                        break

                with open('styles/user_styles.json', 'w') as file:
                    json.dump({"themes": self.themes_data}, file, separators=(',', ':'), indent=4)

                self.master.master.menu.user_themes_menu.delete(theme_to_delete)
                self.themes = []
                self.get_theme_list()
            
    
    def reset_settings(self):
        # delete the saved settings from the json file
        answer = messagebox.askokcancel(title='Reset settings', message='Reset all settings and close the app?')
        if answer:
            self.master.master.reset_data()


    # event methods
    def on_scale_scroll(self, event):
        self.opacity_var.trace('w', self.change_opacity)
        # changing the value of the opacity by scrolling the scale
        if (event.delta > 0 or event.num == 4) and self.opacity_var.get() < self.opacity_max:
            self.opacity_var.set(self.opacity_var.get()+1)
        elif (event.delta < 0 or event.num == 5) and self.opacity_var.get() > self.opacity_min:
            self.opacity_var.set(self.opacity_var.get()-1)

    def change_cursor(self, event, widget):
        # change the cursor when hovering over the objects
        widget.config(cursor='hand2')
    
    def return_cursor(self, event, widget):
        # return the standard cursor when the object is not pointed at
        widget.config(cursor='')
