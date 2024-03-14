import ttkbootstrap as ttk

from .setting_frames import ProgramSettingsTab, StylizationTab, AboutTab


class SettingsFrame(ttk.Notebook):
    def __init__(self, master, start_position, end_position):
        # setup
        super().__init__(master=master)
        self.start_position = start_position
        self.end_position = end_position
        self.height = abs(self.start_position - self.end_position)

        # exit button 
        self.exit_button = ttk.Button(self, text='x', command=self.animate_settings_frame)
        self.exit_button.place(relx=0.98, rely=0, anchor='ne')

        self.exit_button.bind("<Enter>", lambda event, widget=self.exit_button: self.change_cursor(event, widget))
        self.exit_button.bind("<Leave>", lambda event, widget=self.exit_button: self.return_cursor(event, widget))

        # create tabs
        self.create_tabs()

        # place tabs
        self.place_tabs()

        # variables for animation
        self.position = self.start_position
        self.is_start_position = True

        # place main
        self.place(relx=0, rely=self.start_position, relwidth=1, relheight=self.height, anchor='sw')

    def create_tabs(self):
        self.program_settings = ProgramSettingsTab(self)
        self.stylization = StylizationTab(self)
        self.about = AboutTab(self)

    def place_tabs(self):
        self.add(self.program_settings, text='Main Settings')      
        self.add(self.stylization, text='Create theme')
        self.add(self.about, text='About us')


    def animate_settings_frame(self):
        # animation of the settings window
        if self.is_start_position:
            self.appear_settings()
        else:
            self.disappear_settings()

    
    def appear_settings(self):
        # show the settings window
        if self.position < self.end_position:
            self.position += 0.01
            self.place(relx=0, rely=self.position, relwidth=1, relheight=self.height, anchor='sw')
            self.after(1, self.appear_settings)
        else:
            self.is_start_position = False


    def disappear_settings(self):
        # hide the settings window
        if self.position > self.start_position:
            self.position -= 0.01
            self.place(relx=0, rely=self.position, relwidth=1, relheight=self.height, anchor='sw')
            self.after(1, self.disappear_settings)
        else:
            self.is_start_position = True


    # event methods
    def change_cursor(self, event, widget):
        # change the cursor when hovering over the objects
        widget.config(cursor='X_cursor')
    
    def return_cursor(self, event, widget):
        # return the standard cursor when the object is not pointed at
        widget.config(cursor='')
