from tkinter import messagebox
import string
from random import choice


def generate_password(checkbox_values, password_length):
    # initialization of parameters for password generation
    password = ''
    is_lowercase, is_uppercase, is_numbers, is_punctuation = checkbox_values
    lowercase_characters = list(string.ascii_lowercase)
    uppercase_characters = list(string.ascii_uppercase)
    numbers_characters = list(string.digits)
    punctuation_characters = ['!','?','.',',',';','(',')','[',']','{','}','-','+','&','*','%','#','@','$','/','\\',':','=']


    # creating a main list of characters for password generation
    chosen_characters = []
    if is_lowercase:
        chosen_characters += lowercase_characters
    if is_uppercase:
        chosen_characters += uppercase_characters
    if is_numbers:
        chosen_characters += 2 * numbers_characters
    if is_punctuation:
        chosen_characters += punctuation_characters


    # password generation logic
    if not is_lowercase and not is_uppercase and not is_numbers and not is_punctuation:
        messagebox.showwarning(title='warning'.upper(), message='Please select at least one checkbox')
    elif password_length == 0:
        messagebox.showwarning(title='warning'.upper(), message='Please choose a password length greater than 0')
    else:
        if 0 < password_length <= 128:
            if password_length >= 8 and is_lowercase and is_uppercase and is_numbers:
                for _ in range(2):
                    password += choice(lowercase_characters)
                    password += choice(uppercase_characters)
                    password += choice(numbers_characters)
                for _ in range(password_length-len(password)):
                    password += choice(chosen_characters)
            else:
                for _ in range(password_length):
                    password += choice(chosen_characters)
        else:
            messagebox.showwarning(title='warning'.upper(), message='Please choose a password length from 0 to 128')
    
    return password
