import string

from main import get_next_guess, State


def get_result(word, guess):
    result = [State.PRESENT] * 5
    for i in range(5):
        if word[i] == guess[i]:
            result[i] = State.CORRECT
        elif guess[i] not in word:
            result[i] = State.ABSENT

    for i in range(5):
        if result[i] == State.PRESENT:
            result[i] = State.ABSENT
            for j in range(5):
                if guess[i] == word[j] and result[j] != State.CORRECT:
                    result[i] = State.PRESENT

    return result


if __name__ == '__main__':
    f = open("words.txt")
    words = f.readlines()
    f.close()

    for i in range(len(words)):
        words[i] = words[i].rstrip("\n").upper()

    letters = {}
    for letter in list(string.ascii_uppercase):
        letters[letter] = 0

    total_guesses = 0
    successful_solves = 0
    failed_words = []

    for i in range(len(words)):
        word = words[i]
        clean_words = words.copy()
        clean_letters = letters.copy()
        guess = ""
        result = []
        guesses = 0
        success = False
        for j in range(1, 7):
            guess = get_next_guess(clean_words, clean_letters, guess, result)
            result = get_result(word, guess)
            if State.ABSENT not in result and State.PRESENT not in result:
                guesses = j
                success = True
                break

        if success:
            total_guesses += guesses
            successful_solves += 1
        else:
            failed_words.append(word)

        print("Word: {}, tries: {}".format(word, guesses))

    print("{} of {} successful guesses ({}%)".format(successful_solves, len(words), successful_solves / len(words)))
    print("{} average guesses per word".format(total_guesses / successful_solves))
    print("Failed words: {}".format(failed_words))
