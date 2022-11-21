import os
import string
import time
from enum import Enum

import pyperclip
import tweepy
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By


class State(Enum):
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"


def no_match(words, letters, letter, guess, result, i):
    letters[letter] = -1
    for word in words.copy():
        duplicate = False
        for j in range(5):
            if i != j and guess[j] == letter and result[j] != State.ABSENT:
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
        if result[i] == State.ABSENT:
            no_match(words, letters, guess[i], guess, result, i)
        elif result[i] == State.PRESENT:
            partial_match(words, guess[i], i)
        elif result[i] == State.CORRECT:
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


def get_next_guess(words, letters, last_guess, last_result):
    if len(last_result) > 0:
        filter_words(words, letters, last_guess, last_result)

    next_guesses = find_effective_words(words, letters)

    return next_guesses[0]


def solve(browser):
    board = browser.find_element(By.CSS_SELECTOR, "[class*=Board-module_board__]")

    f = open("words.txt")
    words = f.readlines()
    f.close()

    letters = {}
    for letter in list(string.ascii_lowercase):
        letters[letter] = 0

    guess = get_next_guess(words, letters, "", [])
    for i in range(1, 7):
        result = []
        print("Guessing {}".format(guess.rstrip('\n').upper()))
        ActionChains(browser).send_keys(guess).send_keys(Keys.ENTER).perform()
        time.sleep(5)
        row = board.find_element(By.CSS_SELECTOR, "[aria-label='Row {}']".format(i))
        tiles = row.find_elements(By.CSS_SELECTOR, "[aria-roledescription='tile")
        for j in range(0, 5):
            data_state = tiles[j].get_attribute("data-state")
            if data_state == State.CORRECT.value:
                result.append(State.CORRECT)
            elif data_state == State.PRESENT.value:
                result.append(State.PRESENT)
            else:
                result.append(State.ABSENT)
        if State.ABSENT not in result and State.PRESENT not in result:
            print("The word was {}, guessed in {} tries".format(guess.rstrip('\n').upper(), i))
            return
        else:
            guess = get_next_guess(words, letters, guess, result)


def post_result_twitter(result):
    f = open(".twitter_creds")
    creds = f.readlines()
    f.close()

    auth = tweepy.OAuthHandler(creds[0].rstrip('\n'), creds[1].rstrip('\n'))
    auth.set_access_token(creds[2].rstrip('\n'), creds[3].rstrip('\n'))

    api = tweepy.API(auth)
    api.update_status(result)


def auto_solve():
    display = ""
    if os.environ.get('LOCAL_RUN') != "1":
        display = Display()
        display.start()
        pyperclip.set_clipboard("xclip")

    browser = webdriver.Firefox()

    browser.get("https://www.nytimes.com/games/wordle/index.html")

    time.sleep(2)

    try:
        browser.find_element(By.CLASS_NAME, "Modal-module_closeIcon__b4z74").click()
    except NoSuchElementException:
        print("No modal found")

    solve(browser)

    time.sleep(5)
    browser.find_element(By.ID, "share-button").click()
    result = pyperclip.paste()
    print(result)

    browser.close()
    if os.environ.get('LOCAL_RUN') != "1":
        display.stop()
        post_result_twitter(result)


if __name__ == '__main__':
    auto_solve()
