"""this file is a python program which imitates the game show 'Countdown' from channel 4. """

import random
import time
from soupsieve.util import lower
from sphinx.util import matching


# Question One of coursework
def select_characters(testing=False):
    """Asks for user input (9*'c' or 'v') to determine consonants/vowels, and returns 9 characters accordingly

    Input argument 'True' to run a test of the probabilities
    """
    domain: list = []  # this will be used as the array of input characters such as 'ccvcccvvv'
    codomain: list = []  # this list will be used to store the output characters
    consonants = list()  # this list will hold all the consonants to choose from, if the user inputs 'c'
    vowels = list()  # this list will hold all the vowels to choose from, if the user inputs 'v'
    consonants.extend("bbcccddddddffggghhjklllllmmmmnnnnnnnnppppqrrrrrrrrrssssssssstttttttttvwxyz")
    vowels.extend('aaaaaaaaaaaaaaaeeeeeeeeeeeeeeeeeeeeeiiiiiiiiiiiiiooooooooooooouuuuu')

    if testing:
        a = int()
        e = int()
        i = int()
        o = int()
        u = int()

        # change the value of runtimes to change how many samples are observed.
        # higher number should cause output to be closer to target numbers
        runtimes = 1000

        for x in range(67 * runtimes):
            arbitrary_number = random.randint(0, 66)
            if vowels[arbitrary_number] == 'a':
                a += 1
            elif vowels[arbitrary_number] == 'e':
                e += 1
            elif vowels[arbitrary_number] == 'i':
                i += 1
            elif vowels[arbitrary_number] == 'o':
                o += 1
            elif vowels[arbitrary_number] == 'u':
                u += 1
        print('After ' + str(
            67 * runtimes) + ' random numbers generated, these were the relative occurances of each letter, '
                             'averaged over 67 trials')
        print("letter - target - observed value")
        print('a - 15 - ' + str(round(a / runtimes, 2)))
        print('e - 21 - ' + str(round(e / runtimes, 2)))
        print('i - 13 - ' + str(round(i / runtimes, 2)))
        print('o - 13 - ' + str(round(o / runtimes, 2)))
        print('u - 5 - ' + str(round(u / runtimes, 2)))

        if 0.95 * 15 < a / runtimes < 1.05 * 15:
            passed = True
        else:
            passed = False
        if 0.95 * 21 < e / runtimes < 1.05 * 21:
            passed = True
        else:
            passed = False
        if 0.95 * 13 < i / runtimes < 1.05 * 13:
            passed = True
        else:
            passed = False
        if 0.95 * 13 < o / runtimes < 1.05 * 13:
            passed = True
        else:
            passed = False
        if 0.95 * 5 < u / runtimes < 1.05 * 5:
            passed = True
        else:
            passed = False
        if passed:
            print("As all generated values are within 5% of the target probabilities, it can be deduced that the "
                  "correct probabilities are generating the outputs")
            print("Test PASSED")
        else:
            print("Distribution of outputs do not match the target probabilities from the actual game")
            print("Test FAILED")

    else:
        print("Input a ’c’ for a consonant or a ’v’ for a vowel nine times. (hit ENT after each entry)")
        for position in range(9):  # ask for input 9 times
            prompt: str = str(position + 1) + '>>>'
            current_character = input(prompt)
            domain.append(current_character)
            if current_character == 'c':
                rand = random.randint(0, len(consonants)-1)
                codomain.append(consonants[rand])  # choose a random consonant (with weightings)
                consonants.pop(rand)  # removes letter from 'stack' after being chosen
            elif current_character == 'v':
                rand = random.randint(0, len(vowels)-1)
                codomain.append(vowels[rand])  # choose a random vowel (with weightings)
                vowels.pop(rand)  # removes letter from 'stack' after being chosen
            else:  # error handling
                print("Catch exception: invalid input. try entering a 'c' or a 'v' then click enter")
        return ''.join(codomain)


# Question Two of coursework
def dictionary_reader(file_location: str = 'words.txt'):
    """Reads the contents of a file and returns it as a list of strings

    Input argument
    The name of a text file within the same folder as countdown.py
    Defaults to words.txt
    """
    dictionary = open(file_location, 'r')
    words: list = []
    for word in dictionary:
        # filter out the new line punctuation, and add each line to words list
        words.append(word[:-1])
    dictionary.close()
    return words


# Question Three of coursework
def word_lookup(chosen_letters: str):
    """Finds dictionary words made up of the characters input. Returns matching words

    Input argument:
        characters is the 9 randomly selected characters in the game
    """
    # gets the words from the dictionary file in a list format
    all_words = dictionary_reader('words.txt')
    matching_words = list()
    all_letters = list()
    for word in all_words:
        for c in range(len(word)):
            all_letters = [1] * 26
            for chars in chosen_letters:
                all_letters[ord(chars) - 97] += 1
            valid = True
            for letters in word:
                all_letters[ord(lower(letters)) - 97] -= 1
                if all_letters[ord(lower(letters)) - 97] == 0:
                    valid = False
                    break
            if valid:
                matching_words.append(word)
    return list(set(matching_words))


# Question Four of coursework
if __name__ == "__main__":
    characters = select_characters()
    characters_array = [0] * 26
    for char in characters:
        characters_array[ord(char) - 97] += 1
    print("please wait while the computer processes your input...")
    computer_answers = word_lookup(characters)
    longest_computer_answers = []
    longest_computer_answer_length = 0
    user_points = int()
    start_time = int(time.time())
    user_answer = input("You have 30 seconds to guess a word made up of only these letters: " + characters + "  >  ")
    time_to_answer = int(time.time()) - start_time
    user_word_correct_letters = True
    for char in user_answer:
        characters_array[ord(lower(char)) - 97] -= 1
        if characters_array[ord(lower(char)) - 97] == -1:
            user_word_correct_letters = False
            print("You overused the letter '" + char + "' in your answer. You may only use the 9 letters shown above, "
                                                       "which are randomly selected")
    if time_to_answer > 30:
        print("You exceeded the 30 second countdown. Zero points awarded.")
    print("You took " + str(time_to_answer) + " seconds to answer")

    for computer_answer in computer_answers:
        if lower(computer_answer) == lower(user_answer) and user_word_correct_letters:
            if time_to_answer <= 30:
                user_points = len(user_answer)
                print("Your word '" + user_answer + "' is worth " + str(user_points) + " points")
            else:
                print("Your word was correct, but you took too long to answer. ")
                print("You score 0 points")
        if len(computer_answer) == longest_computer_answer_length:
            longest_computer_answers.append(computer_answer)
        elif len(computer_answer) > longest_computer_answer_length:
            longest_computer_answers.clear()
            longest_computer_answers.append(computer_answer)
            longest_computer_answer_length = len(computer_answer)
    if not user_word_correct_letters:
        print("You used letters which were not in the 9 selected characters. You may only use each letter the number "
              "of times it appears")
        print("You score 0 points")
        if user_answer in dictionary_reader():
            print("Your word is found in the dictionary, and would have scored " + str(len(user_answer)) + " points")
    if user_points == 0 and time_to_answer <= 30 and user_word_correct_letters:
        print("Your word was not found in the dictionary file, sorry :(")
        print("You scored 0 points")
    if longest_computer_answer_length == user_points:
        print("Woooo! You got the highest possible scoring answer!")
    print("Here are some of the best answers: ", end="")
    print(", ".join(longest_computer_answers))
    print("Computer scores " + str(longest_computer_answer_length) + " points")
    print()
    print()
    print("Hope you enjoyed playing: ")
    print(
        " .----------------.  .----------------.  .----------------.  .-----------------. .----------------.  .----------------.  .----------------.  .----------------.  .-----------------.")
    print(
        "| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |")
    print(
        "| |     ______   | || |     ____     | || | _____  _____ | || | ____  _____  | || |  _________   | || |  ________    | || |     ____     | || | _____  _____ | || | ____  _____  | |")
    print(
        "| |   .' ___  |  | || |   .'    `.   | || ||_   _||_   _|| || ||_   \|_   _| | || | |  _   _  |  | || | |_   ___ `.  | || |   .'    `.   | || ||_   _||_   _|| || ||_   \|_   _| | |")
    print(
        "| |  / .'   \_|  | || |  /  .--.  \  | || |  | |    | |  | || |  |   \ | |   | || | |_/ | | \_|  | || |   | |   `. \ | || |  /  .--.  \  | || |  | | /\ | |  | || |  |   \ | |   | |")
    print(
        "| |  | |         | || |  | |    | |  | || |  | '    ' |  | || |  | |\ \| |   | || |     | |      | || |   | |    | | | || |  | |    | |  | || |  | |/  \| |  | || |  | |\ \| |   | |")
    print(
        "| |  \ `.___.'\  | || |  \  `--'  /  | || |   \ `--' /   | || | _| |_\   |_  | || |    _| |_     | || |  _| |___.' / | || |  \  `--'  /  | || |  |   /\   |  | || | _| |_\   |_  | |")
    print(
        "| |   `._____.'  | || |   `.____.'   | || |    `.__.'    | || ||_____|\____| | || |   |_____|    | || | |________.'  | || |   `.____.'   | || |  |__/  \__|  | || ||_____|\____| | |")
    print(
        "| |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |")
    print(
        "| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |")
    print(
        " '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' ")
