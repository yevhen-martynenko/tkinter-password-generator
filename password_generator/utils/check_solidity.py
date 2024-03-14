def check_password_solidity(password_value, solidity_lever_value, progressbar):
    # initialization of basic data
    password_solidity_levels = {
        'Very Weak': 25,
        'Weak': 45,
        'Moderate': 65,
        'Strong': 80,
        'Very Strong': 100,
        }
    password_solidity = 0

    password_length = len(password_value)
    has_lowercase = any(char.islower() for char in password_value)
    has_uppercase = any(char.isupper() for char in password_value)
    has_digit = any(char.isdigit() for char in password_value)
    has_punctuation = any(char in '!?.,;()[]}{-+&*%#@$/\\:=' for char in password_value)


    # password solidity check logic
    if has_lowercase:
        password_solidity += 10
    if has_uppercase:
        password_solidity += 10
    if has_digit:
        password_solidity += 15
    if has_punctuation:
        password_solidity += 15

    if password_length >= 64:
        password_solidity += 50
    elif password_length >= 48:
        password_solidity += 45
    elif password_length >= 32:
        password_solidity += 40
    elif password_length >= 28:
        password_solidity += 20
    elif password_length >= 24:
        password_solidity += 15
    elif password_length >= 20:
        password_solidity += 5
    elif password_length >= 16:
        password_solidity -= 5
    elif password_length >= 12:
        password_solidity -= 10
    elif password_length >= 8:
        password_solidity -= 30
    elif password_length >= 4:
        password_solidity -= 40
    else:
        password_solidity = 0


    # create a password output view
    solidity_lever_value.set(password_solidity)
    
    if password_solidity <= password_solidity_levels['Very Weak']:
        progressbar.configure(style='Very_Weak.Horizontal.TProgressbar')
    elif password_solidity <= password_solidity_levels['Weak']:
        progressbar.configure(style='Weak.Horizontal.TProgressbar')
    elif password_solidity <= password_solidity_levels['Moderate']:
        progressbar.configure(style='Moderate.Horizontal.TProgressbar')
    elif password_solidity <= password_solidity_levels['Strong']:
        progressbar.configure(style='Strong.Horizontal.TProgressbar')
    elif password_solidity <= password_solidity_levels['Very Strong']:
        progressbar.configure(style='Very_Strong.Horizontal.TProgressbar')
