import random
import string


def prompt_guess():
    guess = ""
    while len(guess) != 5:
        guess = input('Word guessed: \n')

    return guess


def result_valid(result):
    if len(result) != 5:
        return False

    if set(result).issubset(set('xgy')):
        return True

    return False


def prompt_result():
    result = ""
    while not result_valid(result):
        result = input('Result (x=grey, y=yellow, g=green): \n').lower()

    return result


def no_match(words, letters, letter, guess, result, i):
    letters[letter] = -1
    for word in words.copy():
        duplicate = False
        for j in range(5):
            if i != j and guess[j] == letter and result[j] != "x":
                duplicate = True

        if not duplicate and letter in word:
            words.remove(word)


def partial_match(words, letter, i):
    for word in words.copy():
        if letter not in word:
            words.remove(word)

        if word[i] == letter:
            words.remove(word)


def full_match(words, letter, i):
    for word in words.copy():
        if word[i] != letter:
            words.remove(word)


def filter_words(words, letters, guess, result):
    for i in range(5):
        if result[i] == "x":
            no_match(words, letters, guess[i], guess, result, i)
        elif result[i] == "y":
            partial_match(words, guess[i], i)
        elif result[i] == "g":
            full_match(words, guess[i], i)


def find_effective_words(words, letters):
    for word in words:
        for i in range(5):
            if letters[word[i]] >= 0:
                letters[word[i]] = letters[word[i]] + 1

    most_common = max(letters, key=letters.get)

    filtered_words = []

    for word in words:
        if most_common in word:
            filtered_words.append(word)

    if len(filtered_words) > 5:
        new_letters = letters.copy()
        new_letters[most_common] = -1
        return find_effective_words(filtered_words, new_letters)
    elif len(filtered_words) > 0:
        return filtered_words
    else:
        return words


def print_effective_words(effective_words):
    print("These words contain the most common letters remaining:")
    for i in range(len(effective_words)):
        print(effective_words[i].strip())
    print("\n")


def print_guess(words):
    print("This is a random sampling of remaining words:")
    i = -1
    command = ""
    random_words = random.sample(words, len(words))
    while command != "y":
        for i in range(i + 1, i + 6):
            if i > len(random_words) - 1:
                print("\nthat's all!\n")
                return

            print(random_words[i].strip())

        print("\n")
        command = input("Ready to guess (y/n)? ")


def solve():
    result = ""
    f = open("words.txt")
    words = f.readlines()
    f.close()

    letters = {}
    for letter in list(string.ascii_lowercase):
        letters[letter] = 0

    while result != "ggggg":
        guess = prompt_guess()
        result = prompt_result()

        filter_words(words, letters, guess, result)
        effective_words = find_effective_words(words, letters)

        print_effective_words(effective_words)
        print_guess(words)

    print("That's pretty neat!")


if __name__ == '__main__':
    solve()
