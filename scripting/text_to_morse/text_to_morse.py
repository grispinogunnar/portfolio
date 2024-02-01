import pyperclip

text_morse_dict = {'a': ".-",
                'b': "-...",
                'c': "-.-.",
                'd': "-..",
                'e': ".",
                'f': "..-.",
                'g': "--.",
                'h': "....",
                'i': "..",
                'j': ".---",
                'k': "-.-",
                'l': ".-..",
                'm': "--",
                'n': "-.",
                'o': "---",
                'p': ".--.",
                'q': "--.-",
                'r': ".-.",
                's': "...",
                't': "-",
                'u': "..-",
                'v': "...-",
                'w': ".--",
                'x': "-..-",
                'y': "-.--",
                'z': "--..",
                '1': ".----",
                '2': "..---",
                '3': "...--",
                '4': "....-",
                '5': ".....",
                '6': "-....",
                '7': "--...",
                '8': "---..",
                '9': "----.",
                '0': "-----",
                '.': ".-.-.-",
                ',': "--..--",
                '?': "..--..",
                '\'': ".----.",
                '!': "-.-.--",
                '/': "-.-.",
                '(': "-.--.",
                ')': "-.--.-",
                '&': ".-...",
                ':': "---...",
                ';': "-.-.-.",
                '=': "-...-",
                '+': ".-.-.",
                '-': "-....-",
                '_': "..--.-",
                '\"': ".-..-.",
                '$': "...-..-",
                '@': ".--.-.",
                ' ': " / ",
}


def text_to_morse(text):
    '''Converts an English string into standard Morse Code. Returns the Morse Code string.
    Letters that aren't handled are replaced with a #'''
    english_string = text.casefold()
    morse_string = ''
    for character in english_string:
        char_to_add = str(text_morse_dict.get(character))
        if(char_to_add == "None"):
            char_to_add = '#'
        morse_string += char_to_add + " "
    return morse_string


def user_menu():
    '''Provides an interactive text-based menu for the user.'''
    morse = ''
    while(True):
        user_input = str(input("\nQ: Quit\nM: Convert text to Morse Code\nC: Copy Morse Code to clipboard\nEnter an option: ")).upper()
        if(user_input == "Q"):
            print("Quitting.")
            break
        elif(user_input == "M"):
            morse = text_to_morse(input("Enter English text to convert to Morse Code:\n"))
            print(morse)
        elif(user_input == "C"):
            if(morse == ''):
                print("Cannot copy; No Morse Code has been generated yet!")
            else:
                print("Copied to clipboard.")
                pyperclip.copy(morse)
        else:
            print("Invalid input. Please try again!")
    return


if __name__ == "__main__":
    user_menu()