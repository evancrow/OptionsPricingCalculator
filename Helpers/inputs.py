def integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Please enter a number.')

def float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('Please enter a number.')

def string_input(prompt):
    return input(prompt)

def make_options_input_prompt(options):
    if not options:
        return

    prompt = "Choose from the following options: "

    for index in range(len(options)):
        option = options[index]

        if index == len(options) - 1:
            prompt += option + " "
        else:
            prompt += option + ", "

    return prompt

def options_input(options):
    if not options:
        return

    prompt = make_options_input_prompt(options)
    choice = input(prompt)

    while choice.upper() not in options:
        print("Invalid choice.")
        choice = input(prompt)

    return choice