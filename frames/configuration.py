import ttkbootstrap as ttk

import tkinter as tk
from tkinter import messagebox

from utils import generate_password


class ConfigurationFrame(ttk.Frame):
    def __init__(self, master, output_frame):
        self.output_frame = output_frame

        # setup
        super().__init__(master=master)
        self.config(relief='groove', borderwidth=3)

        # create widgets
        self.create_widgets()

        # place widgets
        self.place_widgets()

        # events
        self.create_events()

        # place main
        self.place(relx=0.02, rely=0.22, relwidth=0.96, relheight=0.76, anchor='nw')

    def create_widgets(self):
        self.label_title = ttk.Label(self, text='Configure your password', anchor='center', font=('Helvetica', 20, 'bold'))

        # initialize additional variables
        self.password_length_min = 0
        self.password_length_max = 128

        # create widgets to determine the length
        self.password_length_var = tk.IntVar(value=0)
        self.password_length_label = ttk.Label(self, text='Choose a length for your password:', font=('Helvetica', 12, 'normal'))
        self.password_length_field = ttk.Spinbox(self,
                                                 from_=self.password_length_min, 
                                                 to=self.password_length_max, 
                                                 increment=1, 
                                                 textvariable=self.password_length_var)
        self.password_length_scale = ttk.Scale(self,
                                               from_=self.password_length_min, 
                                               to=self.password_length_max,
                                               orient='horizontal', 
                                               variable=self.password_length_var,
                                               command=lambda value: self.password_length_var.set(int(float(value))))
        
        # create checkboxes to configure the password
        self.lowercase_check_var = tk.BooleanVar()
        self.lowercase_check = ttk.Checkbutton(
            self, 
            text='Enable lowercase', 
            variable=self.lowercase_check_var, 
            bootstyle="round-toggle")
        self.uppercase_check_var = tk.BooleanVar()
        self.uppercase_check = ttk.Checkbutton(
            self, 
            text='Enable uppercase', 
            variable=self.uppercase_check_var,
            bootstyle="round-toggle")
        self.numbers_check_var = tk.BooleanVar()
        self.numbers_check = ttk.Checkbutton(
            self, 
            text='Enable numbers', 
            variable=self.numbers_check_var,
            bootstyle="round-toggle")
        self.punctuation_check_var = tk.BooleanVar()
        self.punctuation_check = ttk.Checkbutton(
            self, 
            text='Enable punctuation', 
            variable=self.punctuation_check_var,
            bootstyle="round-toggle")

        # create a buttons
        self.generate_button = ttk.Button(self, text='generate'.upper(), command=self.give_data)
        self.reset_button = ttk.Button(self, text='reset'.upper(), command=self.reset_configuration_settings)

    def place_widgets(self):
        # create grid system
        self.columnconfigure((0,1,2,3), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3,4), weight=1, uniform='a')

        # place label
        self.label_title.grid(row=0, column=0, sticky='nesw', columnspan=4)

        # place widgets that determine the length
        self.password_length_label.grid(row=2, column=0, sticky='nesw', columnspan=2, padx=10)
        self.password_length_field.grid(row=2, column=2, sticky='nesw', padx=10, pady=10)
        self.password_length_scale.grid(row=3, column=0, sticky='nesw', columnspan=3, padx=10, pady=10)

        # place checkboxes that configure the password
        self.lowercase_check.grid(row=1, column=3, sticky='nesw')
        self.uppercase_check.grid(row=2, column=3, sticky='nesw')
        self.numbers_check.grid(row=3, column=3, sticky='nesw')
        self.punctuation_check.grid(row=4, column=3, sticky='nesw')

        # place buttons
        self.generate_button.grid(row=4, column=1, sticky='nesw', padx=3, pady=3)
        self.reset_button.grid(row=4, column=2, sticky='nesw', padx=12, pady=9)
    
    def create_events(self):
        # event to change the password length value when scrolling the scale
        self.password_length_scale.bind('<MouseWheel>', self.on_scale_scroll)
        self.password_length_scale.bind('<Button-4>', self.on_scale_scroll)
        self.password_length_scale.bind('<Button-5>', self.on_scale_scroll)

        # events for changing the cursor when hovering over objects
        self.password_length_scale.bind("<Enter>", lambda event, widget=self.password_length_scale: self.change_cursor(event, widget))
        self.lowercase_check.bind("<Enter>", lambda event, widget=self.lowercase_check: self.change_cursor(event, widget))
        self.uppercase_check.bind("<Enter>", lambda event, widget=self.uppercase_check: self.change_cursor(event, widget))
        self.numbers_check.bind("<Enter>", lambda event, widget=self.numbers_check: self.change_cursor(event, widget))
        self.punctuation_check.bind("<Enter>", lambda event, widget=self.punctuation_check: self.change_cursor(event, widget))
        self.generate_button.bind("<Enter>", lambda event, widget=self.generate_button: self.change_cursor(event, widget))
        self.reset_button.bind("<Enter>", lambda event, widget=self.reset_button: self.change_cursor(event, widget))
        
        self.password_length_scale.bind("<Leave>", lambda event, widget=self.password_length_scale: self.return_cursor(event, widget))
        self.lowercase_check.bind("<Leave>", lambda event, widget=self.lowercase_check: self.return_cursor(event, widget))
        self.uppercase_check.bind("<Leave>", lambda event, widget=self.uppercase_check: self.return_cursor(event, widget))
        self.numbers_check.bind("<Leave>", lambda event, widget=self.numbers_check: self.return_cursor(event, widget))
        self.punctuation_check.bind("<Leave>", lambda event, widget=self.punctuation_check: self.return_cursor(event, widget))
        self.generate_button.bind("<Leave>", lambda event, widget=self.generate_button: self.return_cursor(event, widget))
        self.reset_button.bind("<Leave>", lambda event, widget=self.reset_button: self.return_cursor(event, widget))


    def get_check_configuration_values(self):
        # get the values of the checkboxes to configure the password
        is_lowercase = self.lowercase_check_var.get()
        is_uppercase = self.uppercase_check_var.get()
        is_numbers = self.numbers_check_var.get()
        is_punctuation = self.punctuation_check_var.get()

        return is_lowercase, is_uppercase, is_numbers, is_punctuation
    

    def get_password_length_var(self):
        # get the length of the password, check that the password is an integer and that it is in the range from 0 to 128
        try:
            password_length = self.password_length_var.get()
        except tk.TclError:
            messagebox.showwarning(title='warning'.upper(), message='Please enter the password length in integers from 0 to 128')
            password_length = 8
            self.update_password_length(password_length)

            return None
        else:
            return password_length
        

    def update_password_length(self, password_length):
        # in case of an error, reset the password length and Spinbox value
        self.password_length_var.set(password_length)
        self.password_length_field.delete(0, 'end')
        self.password_length_field.insert(0, password_length)


    def give_data(self):
        # generates a password and outputs the password value to a frame
        checkbox_values = self.get_check_configuration_values()
        password_length = self.get_password_length_var()
        
        if password_length != None:
            password = generate_password(checkbox_values, password_length)
            self.output_frame.update_password(password)

    
    def reset_configuration_settings(self):
        # set configuration variables to the default value
        self.lowercase_check_var.set(False)
        self.uppercase_check_var.set(False)
        self.numbers_check_var.set(False)
        self.punctuation_check_var.set(False)
        self.password_length_var.set(0)

        # clear password
        password = ''
        self.output_frame.update_password(password)


    # event methods
    def on_scale_scroll(self, event):
        # changing the value of the password length by scrolling the scale
        if (event.delta > 0 or event.num == 4) and self.password_length_var.get() < self.password_length_max:
            self.password_length_var.set(self.password_length_var.get()+1)
        elif (event.delta < 0 or event.num == 5) and self.password_length_var.get() > self.password_length_min:
            self.password_length_var.set(self.password_length_var.get()-1)

    def change_cursor(self, event, widget):
        # change the cursor when hovering over the objects
        widget.config(cursor='hand2')
    
    def return_cursor(self, event, widget):
        # return the standard cursor when the object is not pointed at
        widget.config(cursor='')
