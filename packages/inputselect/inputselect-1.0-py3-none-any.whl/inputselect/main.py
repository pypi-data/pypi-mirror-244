import time
import keyboard


def generate(index: int):
    return [f"\033[38;5;{int(index)}m", f"\033[48;5;{int(index)}m"]


COLORS = {
    "blank": generate(0),
    "default": generate(0),

    "black": generate(0),
    "grey": generate(240),
    "gray": generate(240),
    "light grey": generate(244),
    "light gray": generate(244),
    "dark grey": generate(236),
    "dark gray": generate(236),

    "white": generate(231),

    "red": generate(160),
    "light red": generate(196),

    "pink": generate(199),
    "light pink": generate(210),

    "orange": generate(202),
    "light orange": generate(208),

    "light yellow": generate(226),
    "yellow": generate(220),

    "light green": generate(118),
    "dark green": generate(22),
    "green": generate(40),

    "teal": generate(49),
    "cyan": ["\033[0;36m", "\033[0;46m"],

    "blue": ["\033[0;34m", "\033[0;44m"],
    "light blue": generate(39),

    "light purple": generate(129),
    "light magenta": generate(129),
    "purple": generate(93),
    "magenta": generate(93)
}

STYLES = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "strikethrough": "\033[9m"
}

DELAY_SECONDS = 0.25
VERSION = "1.0"

DEFAULT_COLORS, ALT_COLORS = ["blue", "blank"], ["yellow", "blank"]
Q_MARK = f"[{COLORS.get('yellow')[0]}?{STYLES['reset']}] "

EXIT_SEQUENCE = "-EXIT-"


def List(message: str = "", choices=("cow", "dog", "horse", "camel"), separator: str = " ", spin_speed: int = 0, colors=DEFAULT_COLORS, font_effects=[]):

    choice_place = 0
    len_choices = len(choices)

    def update():

        output = ""
        x = 0
        for x in range(len_choices):

            # checks if any given choice is the one the user is resting on
            if x == choice_place:
                output += COLORS.get(colors[0])[0] + COLORS.get(colors[1])[1]

                # adds bold if needed
                if "bold" in font_effects:
                    output += STYLES["bold"]

                # adds italic if needed
                if "italic" in font_effects:
                    output += STYLES["italic"]
                
                # adds underline if needed
                if "underline" in font_effects:
                    output += STYLES["underline"]

                # adds strikethrough if needed
                if "strikethrough" in font_effects:
                    output += STYLES["strikethrough"]

                # resets all styles and adds a separator
                output += str(choices[x]) + STYLES["reset"] + separator

            else:
                output += str(choices[x]) + separator

            x += 1

        time.sleep(DELAY_SECONDS)

        print(Q_MARK + message + output, end="\r")

    update()

    while True:
        # if the user is not in spin_speed mode
        if spin_speed == 0:
            # checks for rightwards movement
            if keyboard.is_pressed("right"):
                choice_place = (choice_place + 1) % len_choices
                update()

            # checks for leftwards movement
            if keyboard.is_pressed("left"):
                choice_place = (choice_place - 1) % len_choices
                update()

        # if the user is in positive spin_speed mode
        elif spin_speed > 0:
            time.sleep(spin_speed / 20)
            choice_place = (choice_place + 1) % len_choices
            update()

        # if the user is in negative spin_speed mode
        elif spin_speed < 0:
            time.sleep(abs(spin_speed / 20))
            choice_place = (choice_place - 1) % len_choices
            update()

        # checks if the user seleced an option
        if keyboard.is_pressed("enter"):
            update()

            print("", end="\n")
            return choices[choice_place]


def Slider(message: str = "pick a letter: ", choices=("A", "B", "C", "D", "E"), spin_speed: int = 0, colors=DEFAULT_COLORS, wrap=True, font_effects=[]):

    choice_place = 0
    len_choices = len(choices)

    longest = choices[[len(str(s)) for s in choices].index(
        max([len(str(s)) for s in choices]))]

    def update():

        output = ""

        text_color = colors[0]
        bg_color = colors[1]

        # adds special colors
        output += COLORS.get(text_color)[0] + COLORS.get(bg_color)[1]

        # adds bold if needed
        if "bold" in font_effects:
            output += STYLES["bold"]

        # adds italic if needed
        if "italic" in font_effects:
            output += STYLES["italic"]
        
        # adds underline if needed
        if "underline" in font_effects:
            output += STYLES["underline"]

        # adds strikethrough if needed
        if "strikethrough" in font_effects:
            output += STYLES["strikethrough"]

        # resets all styles
        output += str(choices[choice_place]) + STYLES["reset"]

        # prevents an error that happens when you go up to the highest value and come down
        output += " " * (len(str(longest)) - len(str(choices[choice_place])))

        time.sleep(DELAY_SECONDS)
        print(Q_MARK + message + output, end="\r")

    update()

    while True:
        # if the user is not in spin_speed mode
        if spin_speed == 0:
            # checks for up key press, showing the user wants to go up
            if keyboard.is_pressed("up"):
                choice_place += 1
                if wrap is True:
                    choice_place %= len_choices
                else:
                    if choice_place > len_choices-1:
                        choice_place -= 1

                update()

            # checks for down key press, showing the user wants to go down
            if keyboard.is_pressed("down"):
                choice_place -= 1
                if wrap is True:
                    choice_place %= len_choices
                else:
                    if choice_place < 0:
                        choice_place += 1

                update()

        # if the user is in positive spin_speed mode
        elif spin_speed > 0:
            time.sleep(spin_speed / 20)

            choice_place += 1
            if wrap is True:
                choice_place %= len_choices
            else:
                if choice_place < 0:
                    choice_place -= 1

            update()

        # if the user is in negative spin_speed mode
        elif spin_speed < 0:
            time.sleep(abs(spin_speed / 20))

            choice_place -= 1
            if wrap is True:
                choice_place %= len_choices
            else:
                if choice_place < 0:
                    choice_place += 1

            update()

        # checks if the user seleced an option
        if keyboard.is_pressed("enter"):
            update()

            print("", end="\n")
            return choices[choice_place]


def Checkbox(message: str = "pick an animal: ", choices=["cow", "dog", "horse", "camel"], separator: str = " ", min_choices=2, max_choices=3, colors=DEFAULT_COLORS, alt_colors=ALT_COLORS, font_effects=[]):

    choice_place = 0

    # maximum select limit
    if max_choices is None:
        max_choices = len(choices)

    # minimum select limit
    if min_choices is None:
        min_choices = 0

    choices.append(EXIT_SEQUENCE)

    len_choices = len(choices)

    total_selected = 0
    chosen_places = []

    def update():

        output = ""
        x = 0
        for x in range(len_choices):

            # checks if any given choice is the one the user is resting on
            if x == choice_place:

                if x == choices.index(EXIT_SEQUENCE):
                    # red text if the option is "--exit--"
                    output += COLORS.get("light red")[0]
                else:
                    # adds normal formatted colors otherwise
                    output += COLORS.get(colors[0])[0] + \
                        COLORS.get(colors[1])[1]

                # adds a checked box if the user has selected this option
                if choice_place in chosen_places:
                    # but not if it is the exit key
                    if not x == choices.index(EXIT_SEQUENCE):
                        output += "[X] "

                else:
                    # adds a blank box if the user has not selected this option
                    if not x == choices.index(EXIT_SEQUENCE):
                        output += "[ ] "

                # adds bold if needed
                if "bold" in font_effects:
                    output += STYLES["bold"]

                # adds italic if needed
                if "italic" in font_effects:
                    output += STYLES["italic"]
                
                # adds underline if needed
                if "underline" in font_effects:
                    output += STYLES["underline"]

                # adds strikethrough if needed
                if "strikethrough" in font_effects:
                    output += STYLES["strikethrough"]

                # resets all styles and adds a separator
                output += str(choices[x]) + STYLES["reset"] + separator

            # checks if this option has already been selected
            elif x in chosen_places:
                output += COLORS.get(alt_colors[0])[0] + \
                    COLORS.get(alt_colors[1])[1] + "[X] "

                # adds bold if needed
                if "bold" in font_effects:
                    output += STYLES["bold"]

                # adds italic if needed
                if "italic" in font_effects:
                    output += STYLES["italic"]
                
                # adds underline if needed
                if "underline" in font_effects:
                    output += STYLES["underline"]

                # adds strikethrough if needed
                if "strikethrough" in font_effects:
                    output += STYLES["strikethrough"]

                # resets all styles and adds a separator
                output += str(choices[x]) + STYLES["reset"] + separator

            else:
                if not x == choices.index(EXIT_SEQUENCE):
                    # adds a blank box and the plain version of the choice
                    output += "[ ] " + str(choices[x]) + separator

                else:
                    output += str(choices[x]) + separator

            x += 1

        # if the user needs 1 more selections to escape...
        if (min_choices - len(chosen_places)) == 1:

            # ...end message is made to the user so
            end_message = COLORS.get("light red")[
                0] + " (1 more)" + STYLES["reset"]

        # if the user needs more than 1 selections to escape...
        elif (min_choices - len(chosen_places)) > 1:

            # ...end message is made to the user so
            end_message = COLORS.get("light red")[
                0] + f" ({min_choices-len(chosen_places)} more)" + STYLES["reset"]

        # if the user doesn't need anymore selections to escape...
        elif (min_choices - len(chosen_places)) < 1:

            # ...end message is made to the user so
            end_message = COLORS.get("light red")[
                0] + " (0 more)" + STYLES["reset"]

        time.sleep(DELAY_SECONDS)

        print(Q_MARK + message + output + end_message + (" "*13), end="\r")

    update()

    while True:

        # checks for rightwards movement
        if keyboard.is_pressed("right"):
            choice_place = (choice_place + 1) % len_choices
            update()

        # checks for leftwards movement
        if keyboard.is_pressed("left"):
            choice_place = (choice_place - 1) % len_choices
            update()

        # checks if the user seleced an option
        if keyboard.is_pressed("enter"):

            # checks if the choice is unique and not --exit--
            if (choice_place not in chosen_places):

                # checks if the user hasn't gone over their choice limit
                if len(chosen_places) < max_choices:
                    if not choice_place == choices.index(EXIT_SEQUENCE):
                        total_selected += 1
                        chosen_places.append(choice_place)

            else:
                chosen_places.remove(choice_place)
                total_selected -= 1

            update()

            # allows the user to end
            if (choice_place == choices.index(EXIT_SEQUENCE)) and total_selected >= min_choices:
                print("", end="\n")

                product_list = []
                for c in chosen_places:
                    product_list.append(choices[c])

                return product_list

