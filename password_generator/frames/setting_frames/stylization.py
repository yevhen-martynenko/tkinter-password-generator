import ttkbootstrap as ttk
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog

import tkinter as tk 
from tkinter import messagebox
from random import choice, randint
import string
import json


class StylizationTab(ttk.Frame):
    def __init__(self, master):
        # setup
        super().__init__(master=master)

        # set default value
        self.color_dictionary = {
            "primary": '#ffffff',
            "secondary": '#ffffff',
            "success": '#ffffff',
            "info": '#ffffff',
            "warning": '#ffffff',
            "danger": '#ffffff',
            "light": '#ffffff',
            "dark": '#ffffff',
            "bg": '#ffffff',
            "fg": '#ffffff',
            "selectbg": '#ffffff',
            "selectfg": '#ffffff',
            "border": '#ffffff',
            "inputfg": '#ffffff',
            "inputbg": '#ffffff',
            "active": '#ffffff',
        }
        self.required_colors = ["primary","secondary","success","info","warning","danger","light","dark","bg","fg","selectbg","selectfg","border","inputfg","inputbg","active"]
        self.item_heigth = 30
        self.items_number = len(self.required_colors) / 2
        self.list_heigth = self.items_number * self.item_heigth
        self.other_widgets_heigth = 0

        # create widgets
        self.create_widgets()

        # place widgets
        self.place_widgets()

        # create a frames to require a color
        self.create_frames()

        # create events
        self.create_events()

        # create scrolling
        self.scrolling()

        # events 
        self.bind('<Configure>', self.update_size)

    def create_widgets(self):
        # create title
        self.title_label = ttk.Label(self, text='Create theme', anchor='center', font=('Helvetica', 20, 'bold'))

        # create widgets to define a name
        self.name_label = ttk.Label(self, text='Write the name of your theme:', anchor='center', font=('Helvetica', 12, 'normal'))
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self, textvariable=self.name_var)

        # create widgets to define a mode
        self.theme_mode_var = tk.BooleanVar(value=True)
        self.theme_mode_label = ttk.Label(self, text='Select a mode for the theme', font=('Helvetica', 12, 'normal'))
        self.light_mode_radio = ttk.Radiobutton(self, text='Light', value=True, variable=self.theme_mode_var)
        self.dark_mode_radio = ttk.Radiobutton(self, text='Dark', value=False, variable=self.theme_mode_var)

        # create buttons
        self.fill_button = ttk.Button(self, text='Fill with random data', command=self.fill_with_random_data)
        self.save_button = ttk.Button(self, text='Save', command=self.write_data)

        # create a canvas
        self.scroll_canvas = tk.Canvas(self, scrollregion=(0,0,self.winfo_width(),self.list_heigth+self.other_widgets_heigth))

        # create a mainframe
        self.color_frame = ttk.Frame(self, relief='groove', border=5)

    def place_widgets(self):
        # place title
        self.title_label.place(relx=0, y=self.other_widgets_heigth, relwidth=1, height=30, anchor='nw')
        self.other_widgets_heigth += 45

        # place widgets to define a name
        self.name_label.place(relx=0, y=self.other_widgets_heigth, relwidth=0.5, height=30, anchor='nw')
        self.name_entry.place(relx=0.55, y=self.other_widgets_heigth, relwidth=0.4, height=30, anchor='nw')
        self.other_widgets_heigth += 40

        # place widgets to define a mode
        self.theme_mode_label.place(relx=0.1, y=self.other_widgets_heigth, relwidth=0.5, height=30, anchor='nw')
        self.light_mode_radio.place(relx=0.55, y=self.other_widgets_heigth, relwidth=0.1, height=30, anchor='nw')
        self.dark_mode_radio.place(relx=0.75, y=self.other_widgets_heigth, relwidth=0.1, height=30, anchor='nw')
        self.other_widgets_heigth += 40

        # place buttons
        self.fill_button.place(relx=0.1, y=self.other_widgets_heigth, relwidth=0.35, height=30, anchor='nw')
        self.save_button.place(relx=0.55, y=self.other_widgets_heigth, relwidth=0.35, height=30, anchor='nw')
        self.other_widgets_heigth += 50

        # place canvas
        self.scroll_canvas.place(relx=0, y=self.other_widgets_heigth, relwidth=1, anchor='nw')

        # update scrollregion for scroll canvas 
        self.scroll_canvas.configure(scrollregion=(0,0,self.winfo_width(),self.list_heigth+self.other_widgets_heigth+10))


    def create_frames(self):
        # logic for creating and positioning frames
        counter = 0
        padding = 10
        for index, item in enumerate(self.required_colors):
            if index % 2 == 0:
                self.create_item(index, item).place(relx=0, y=counter*self.item_heigth + padding, relwidth=0.5, height=self.item_heigth, anchor='nw')
            elif index % 2 == 1:
                self.create_item(index, item).place(relx=0.5, y=counter*self.item_heigth + padding, relwidth=0.5, height=self.item_heigth, anchor='nw')
                counter += 1
                padding += 10

    def create_item(self, index, item):
        # create a frame and objects in it
        frame = ttk.Frame(self.color_frame)

        # widgets
        label = ttk.Label(frame, text=f'choose {item} color', font=('Helvetica', 12, 'normal'))
        label.place(relx=0.05, rely=0, relwidth=0.55, relheight=1, anchor='nw')

        color = self.color_dictionary[item]
        color_lable = ttk.Label(frame, background=color)
        color_lable.place(relx=0.55, rely=0, relwidth=0.40, relheight=1, anchor='nw')

        color_button = ttk.Button(frame, text=f'{index}', command=lambda: self.choose_color(item))
        color_button.place(relx=0.65, rely=0, relwidth=0.20, relheight=1, anchor='nw')
        color_button.bind("<Enter>", lambda event, widget=color_button: self.change_cursor(event, widget))
        color_button.bind("<Leave>", lambda event, widget=color_button: self.return_cursor(event, widget))

        return frame


    def create_events(self):
        # events for changing the cursor when hovering over objects
        self.light_mode_radio.bind("<Enter>", lambda event, widget=self.light_mode_radio: self.change_cursor(event, widget))
        self.light_mode_radio.bind("<Leave>", lambda event, widget=self.light_mode_radio: self.return_cursor(event, widget))
        self.dark_mode_radio.bind("<Enter>", lambda event, widget=self.dark_mode_radio: self.change_cursor(event, widget))
        self.dark_mode_radio.bind("<Leave>", lambda event, widget=self.dark_mode_radio: self.return_cursor(event, widget))
        self.save_button.bind("<Enter>", lambda event, widget=self.save_button: self.change_cursor(event, widget))
        self.save_button.bind("<Leave>", lambda event, widget=self.save_button: self.return_cursor(event, widget))
        self.fill_button.bind("<Enter>", lambda event, widget=self.fill_button: self.change_cursor(event, widget))
        self.fill_button.bind("<Leave>", lambda event, widget=self.fill_button: self.return_cursor(event, widget))


    # event methods
    def change_cursor(self, event, widget):
        # change the cursor when hovering over the objects
        widget.config(cursor='hand2')
    
    def return_cursor(self, event, widget):
        # return the standard cursor when the object is not pointed at
        widget.config(cursor='')


    def scrolling(self):
        # create scroll
        self.scroll_canvas.create_window(
            (0,0), 
            window=self.color_frame, 
            anchor='nw', 
            width=self.winfo_width(), 
            height=self.list_heigth+self.other_widgets_heigth)

        # scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.scroll_canvas.yview)
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

    def update_size(self, event):
        # create a scroll by moving the mouse wheel
        if self.list_heigth+self.other_widgets_heigth >= self.winfo_height():
            self.scroll_canvas.bind_all('<MouseWheel>', lambda event: self.scroll_canvas.yview_scroll(-int(event.delta/90), 'units'))
            self.scroll_canvas.bind_all('<Button-4>', lambda event: self.scroll_canvas.yview_scroll(-1, 'units'))
            self.scroll_canvas.bind_all('<Button-5>', lambda event: self.scroll_canvas.yview_scroll(1, 'units'))

            self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        else:
            self.scroll_canvas.unbind_all('<MouseWheel>')
            self.scroll_canvas.unbind_all('<Button-4>')
            self.scroll_canvas.unbind_all('<Button-5>')
            self.scrollbar.place_forget()
            
        self.scroll_canvas.create_window(
            (0,0), 
            window=self.color_frame, 
            anchor='nw', 
            width=self.winfo_width(), 
            height=self.list_heigth+self.other_widgets_heigth)


    def choose_color(self, color):
        # create a ColorChooser window and get the hex value
        color_window =  ColorChooserDialog()
        color_window.show()
        color_code = color_window.result

        try:
            self.color_dictionary[color] = color_code[2]
        except TypeError:
            self.color_dictionary[color] = '#ffffff'

        # change the background color of the label that shows the selected color
        padding = 10
        index = self.required_colors.index(color)
        if index % 2 == 0:
            self.create_item(index, color).place(relx=0, y=(self.item_heigth+padding) * (int(index/2)) + padding, relwidth=0.5, height=self.item_heigth,anchor='nw')
        elif index % 2 == 1:
            self.create_item(index, color).place(relx=0.5, y=(self.item_heigth+padding) * (int(index/2)) + padding, relwidth=0.5, height=self.item_heigth, anchor='nw')


    def write_data(self):
        # write data to a json file
        name = self.name_entry.get()

        if not name:
            messagebox.showwarning(title='Enter a name', message='You need to write a theme name')
            return

        mode = "light" if self.theme_mode_var.get() else "dark"
        colors = self.color_dictionary

        try:
            with open('styles/user_styles.json', 'r') as file:
                data = json.load(file)
                themes = data.get("themes", [])
        except Exception:
            themes = []

        themes.append({name: {"type": mode, "colors": colors}})
        with open('styles/user_styles.json', 'w') as file:
            json.dump({"themes": themes}, file, separators=(',', ':'), indent=4)
        
        self.master.master.menu.get_user_themes()
        self.master.program_settings.get_theme_list()


    def fill_with_random_data(self):
        # generate a random name
        vowel_letters = ['e', 'y', 'u', 'i', 'o', 'a', 'e', 'y', 'u', 'i', 'o', 'a', 'ey', 'ou', 'oy', 'ea', 'ai', 'oo', 'ee', '', '', '', '', '']
        consonant_letters = ['q', 'w', 'r', 't', 'p', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'ch', 'sh', 'th', 'ng', '', '', '', '', '']
        random_name = "".join((choice(consonant_letters) + choice(vowel_letters)) for _ in range(randint(1, 4)))
        if random_name == '':
            random_name = 'secret_name'

        # generate a random mode
        random_mode = bool(randint(0,1))

        # generate a random color
        hex_characters =  list(string.digits) + ['a', 'b', 'c', 'd', 'e']
        random_colors = [f'#{"".join([choice(hex_characters) for _ in range(0,6)])}' for _ in range(len(self.required_colors))]

        # record the data
        self.name_var.set(random_name)
        self.theme_mode_var.set(random_mode)
        self.color_dictionary = {color: random_colors[index] for index, color in enumerate(self.required_colors)}
        self.create_frames()
