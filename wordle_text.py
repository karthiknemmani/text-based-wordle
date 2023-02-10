# Name:
# UTEID:
# replace <NAME> with your name and delete this line.
#
# On my honor, <NAME>, this programming assignment is my own work
# and I have not provided this code to any other student.

import random
import string

def main():
    """ Plays a text based version of Wordle.
        1. Read in the words that can be choices for the secret word
        and all the valid words. The secret words are a subset of
        the valid words.
        2. Explain the rules to the player.
        3. Get the random seed from the player if they want one.
        4. Play rounds until the player wants to quit.
    """
    secret_words, all_words = get_words()
    welcome_and_instructions()
    play_wordle(secret_words, all_words)



def welcome_and_instructions():
    """
    Print the instructions and set the initial seed for the random
    number generator based on user input.
    """
    print('Welcome to Wordle.')
    instructions = input('\nEnter y for instructions, anything else to skip: ')
    if instructions == 'y':
        print('\nYou have 6 chances to guess the secret 5 letter word.')
        print('Enter a valid 5 letter word.')
        print('Feedback is given for each letter.')
        print('G indicates the letter is in the word and in the correct spot.')
        print('O indicates the letter is in the word but not that spot.')
        print('- indicates the letter is not in the word.')
    set_seed = input('\nEnter y to set the random seed, anything else to skip: ')
    if set_seed == 'y':
        random.seed(int(input('\nEnter number for initial seed: ')))


def get_words():
    """ Read the words from the dictionary files.
        We assume the two required files are in the current working directory.
        The file with the words that may be picked as the secret words is
        assumed to be names secret_words.txt. The file with the rest of the
        words that are valid user input but will not be picked as the secret
        word are assumed to be in a file named other_valid_words.txt.
        Returns a sorted tuple with the words that can be
        chosen as the secret word and a set with ALL the words,
        including both the ones that can be chosen as the secret word
        combined with other words that are valid user guesses.
    """
    temp_secret_words = []
    with open('secret_words.txt', 'r') as data_file:
        all_lines = data_file.readlines()
        for line in all_lines:
            temp_secret_words.append(line.strip().upper())
    temp_secret_words.sort()
    secret_words = tuple(temp_secret_words)
    all_words = set(secret_words)
    with open('other_valid_words.txt', 'r') as data_file:
        all_lines = data_file.readlines()
        for line in all_lines:
            all_words.add(line.strip().upper())
    return secret_words, all_words

def play_wordle(secret_words, all_words):
    """Acts as the game text interface and plays until user decides not to"""
    play = True
    while play:
        correct_word = random.choice(secret_words)
        guessed = False
        guesses = []
        num_guesses = 0
        alphabets = list(string.ascii_uppercase)
        guess_accuracies = []
        while not guessed and num_guesses < 6:
            guess_word = input('\nEnter your guess. A 5 letter word: ')
            print()
            guess_word = guess_word.upper()
            # check if word is valid
            if guess_word in all_words:
                guesses.append(guess_word)
                accuracy = guess_eval(guess_word, correct_word)
                guess_accuracies.append((accuracy, guess_word))
                guess_output(guess_word, guess_accuracies, alphabets)
                num_guesses += 1
                if guess_word == correct_word:
                    guessed = True
            else:
                print(f'{guess_word} is not a valid word. Please try again.')
        play = finish_game(num_guesses, guessed, correct_word)
    
def guess_output(guess_word, guess_accuracies, alphabets):
    for guess in guess_accuracies:
        print(guess[0])
        print(guess[1])
    for letter in guess_word:
        alphabets.remove(letter) if letter in alphabets else None
    print('\nUnused letters:',end='')
    for alph in alphabets:
        print(f' {alph}', end='')
    print()
        

def create_word_dict(correct_word):
    """Creates a dictionary of the letters in the correct word to 
    evaluate guess"""
    word_chars = {}
    for c in correct_word:
        if c in word_chars.keys():
            word_chars.update({c: word_chars.get(c) + 1})
        else:
            word_chars.update({c: 1})
    return word_chars

def guess_eval(guess_word, correct_word):
    """ Evaluates a guess given the guess and the correct word """
    word_check = ['-', '-', '-', '-', '-'] # check which letters are correct
    correct_word_chars = create_word_dict(correct_word)
    for i in range(len(guess_word)):
        if guess_word[i] == correct_word[i]:
            word_check[i] = 'G'
            if correct_word_chars.get(guess_word[i]) == 1:
                del correct_word_chars[guess_word[i]]
            else:
                correct_word_chars.update({guess_word[i]: 
                    correct_word_chars.get(guess_word[i]) - 1})
        elif (guess_word[i] in correct_word) and (
            guess_word[i] in correct_word_chars.keys()):
            if (correct_word_chars.get(guess_word[i]) > 0):
                correct_word_chars.update({guess_word[i]: 
                    correct_word_chars.get(guess_word[i]) - 1})
                word_check[i] = 'O'
    return ''.join(word_check)

def finish_game(num_guesses, guessed, correct_word):
    """Given whether the word was guessed or not (and if so, 
    how many guesses), this provides proper end-of-game output"""
    if guessed:
        print('\nYou win.', end=' ')
        if num_guesses == 1:
            print('Genius!')
        elif num_guesses == 2:
            print('Magnificent!')
        elif num_guesses == 3:
            print('Impressive!')
        elif num_guesses == 4:
            print('Splendid!')
        elif num_guesses == 5:
            print('Great!')
        elif num_guesses == 6:
            print('Phew!')
    else:
        print(f'\nNot quite. The secret word was {correct_word}.')
    play_again = input(
        '\nDo you want to play again? Type Y for yes: ').upper()
    return True if play_again == 'Y' else False
    

if __name__ == '__main__':
    main()
