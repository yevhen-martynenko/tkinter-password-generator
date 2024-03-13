import ttkbootstrap as ttk

import webbrowser


class AboutTab(ttk.Frame):
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
        # create widgets
        self.title_label = ttk.Label(self, text='About us', font=('Helvetica', 20, 'bold'))

        self.text_label = ttk.Label(self, text='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ultrices justo vel enim imperdiet, vel egestas urna fermentum. Etiam ligula lacus, auctor porta vulputate a, volutpat sed nibh. In sit amet eleifend dui. Proin euismod ante non mattis finibus. Phasellus ut semper tellus. Fusce dignissim felis arcu, ac malesuada odio ullamcorper ac. Praesent egestas velit ut egestas bibendum. Vestibulum volutpat massa sapien, vitae iaculis arcu vulputate vel. Donec eu efficitur odio, at euismod nisi. Nulla vitae fringilla lectus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam pharetra laoreet lacus, nec tincidunt massa egestas sed.', wraplength=650, font=('Helvetica', 12, 'normal'))

        self.link_button = ttk.Button(self, text='Github', command=lambda: webbrowser.open_new(r"https://github.com/yevhen-martynenko"))

    def place_widgets(self):
        # place widgets
        self.title_label.pack(anchor='center', pady=20)
        self.text_label.pack(fill='both')
        self.link_button.pack(expand=True)

    def create_events(self):
        # events for changing the cursor when hovering over objects
        self.link_button.bind("<Enter>", lambda event, widget=self.link_button: self.change_cursor(event, widget))
        self.link_button.bind("<Leave>", lambda event, widget=self.link_button: self.return_cursor(event, widget))


    # event methods
    def change_cursor(self, event, widget):
        # change the cursor when hovering over the objects
        widget.config(cursor='hand2')
    
    def return_cursor(self, event, widget):
        # return the standard cursor when the object is not pointed at
        widget.config(cursor='')
