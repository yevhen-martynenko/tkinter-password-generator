import ttkbootstrap as ttk
import ttkbootstrap.constants as bcons

import tkinter as tk

from utils import check_password_solidity


class OutputFrame(ttk.Frame):
    def __init__(self, master, password_var):
        self.password_var = password_var

        # setup
        super().__init__(master=master)

        # create widgets
        self.create_widgets()

        # place widgets
        self.place_widgets()

        # events
        self.create_events()

        # place main
        self.place(relx=0, rely=0, relwidth=1, relheight=0.2, anchor='nw')

    def create_widgets(self):
        # create widgets for output
        self.frame_output = ttk.Frame(self, relief='groove') 
        self.entry_output = ttk.Entry(self.frame_output, textvariable=self.password_var, font=('Helvetica', '18', 'bold'))
        self.button_copy = ttk.Button(self.frame_output, text='copy'.upper(), command=self.copy_to_clipboard)

        # create widgets for solidity check
        self.frame_solidity = ttk.Frame(self, relief='groove')
        self.solidity_level_var = tk.IntVar(value=0)
        self.solidity_level = ttk.Progressbar(self.frame_solidity, maximum=100,
                                              orient='horizontal', variable=self.solidity_level_var,
                                              mode='determinate', bootstyle=bcons.DARK)

        # checking whether the password has been changed to run the solidity check function
        self.password_var.trace('w', lambda name, index, mode, password_var=self.password_var, solidity_lever_var=self.solidity_level_var: 
                                check_password_solidity(password_var.get(), solidity_lever_var, self.solidity_level))

    def place_widgets(self):
        # place widgets for output
        self.entry_output.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')
        self.button_copy.place(relx=0.89, rely=0.1, relwidth=0.1, relheight=0.8, anchor='nw')
        self.frame_output.place(relx=0, rely=0, relwidth=1, relheight=0.75, anchor='nw')

        # place widgets for solidity check
        self.solidity_level.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')
        self.frame_solidity.place(relx=0, rely=0.75, relwidth=1, relheight=0.25, anchor='nw')

    def create_events(self):
        # events for changing the cursor when hovering over objects
        self.button_copy.bind("<Enter>", lambda event, widget=self.button_copy: self.change_cursor(event, widget))
        self.button_copy.bind("<Leave>", lambda event, widget=self.button_copy: self.return_cursor(event, widget))

        # events for changing the cursor when hovering over the solidity levelProgressbar
        self.solidity_level.bind("<Enter>", lambda event, widget=self.solidity_level: self.change_cursor_progressbar(event, widget))
        self.solidity_level.bind("<Leave>", lambda event, widget=self.solidity_level: self.return_cursor_progressbar(event, widget))
        self.solidity_level.bind("<ButtonRelease-1>", self.choose_best_values)


    def copy_to_clipboard(self):
        # copy the password to the clipboard
        password = self.password_var.get()
        self.clipboard_clear()
        self.clipboard_append(password)
        self.update()
        self.update_password('')

    
    def update_password(self, password):
        # reset the password and Entry value
        self.password_var.set(password)
        self.entry_output.delete(0, 'end')
        self.entry_output.insert(0, password)

    
    # event methods
    def change_cursor(self, event, widget):
        # change the cursor when hovering over the objects
        widget.config(cursor='hand2')
    
    def return_cursor(self, event, widget):
        # return the standard cursor when the object is not pointed at
        widget.config(cursor='')

    def change_cursor_progressbar(self, event, widget):
        # change the cursor when hovering over the objects
        widget.config(cursor='plus')
    
    def return_cursor_progressbar(self, event, widget):
        # return the standard cursor when the object is not pointed at
        widget.config(cursor='')

    def choose_best_values(self, event):
        # set the best values for password generation
        self.master.configuration.lowercase_check_var.set(True)
        self.master.configuration.uppercase_check_var.set(True)
        self.master.configuration.numbers_check_var.set(True)
        self.master.configuration.punctuation_check_var.set(True)
        self.master.configuration.password_length_var.set(32)
