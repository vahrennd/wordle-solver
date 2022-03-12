def filter_possible_words():
    f = open("words_alpha.txt", "r")
    lines = f.readlines()
    f.close()

    words = []
    for line in lines:
        if len(line) == 6:
            words.append(line)

    output = open('words.txt', 'w')
    output.writelines(words)
    output.close()


def prompt_guess():
    guess = ""
    while len(guess) != 5:
        guess = input('Word guessed: \n')

    return guess


def result_valid(result):
    if len(result) != 5:
        return False

    valid = set('xgy')
    if set(result).issubset(valid):
        return True

    return False


def prompt_result():
    result = ""
    while not result_valid(result):
        result = input('Result (x=grey, y=yellow, g=green): \n').lower()

    return result


def no_match(words, letter, guess, result, i):
    for word in words.copy():
        duplicate = False
        for j in range(5):
            if i != j and result[j] == "g" and guess[j] == letter:
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


def filter_words(words, guess, result):
    for i in range(5):
        if result[i] == "x":
            no_match(words, guess[i], guess, result, i)

        if result[i] == "y":
            partial_match(words, guess[i], i)

        if result[i] == "g":
            full_match(words, guess[i], i)


def print_guess(words):
    i = -1
    command = ""
    while command != "y":
        for i in range(i + 1, i + 6):
            if i > len(words) - 1:
                print("that's all!")
                return

            print(words[i].strip())

        command = input("Ready to guess (y/n)? ")


def solve():
    result = ""
    f = open("words.txt")
    words = f.readlines()
    f.close()

    while result != "ggggg":
        guess = prompt_guess()
        result = prompt_result()

        filter_words(words, guess, result)

        print_guess(words)

    print("That's pretty neat!")


if __name__ == '__main__':
    solve()
