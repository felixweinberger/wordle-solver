import csv
from collections import Counter


def get_word_list():
    """
    Returns a list of(word, freq) tuples of 5-letter words in the english dictionary.
    The words originate from the dictionary, while their frequencies are based on
    number of occurences in the world wide web. Where a word does not occur online, its
    frequency is marked 0.
    """
    five_letter_word_freqs = {}
    with open("unigram_freq.csv") as word_frequencies:
        freq_reader = csv.reader(word_frequencies, delimiter=",")
        # skip the header
        next(freq_reader)
        for row in freq_reader:
            if len(row[0]) == 5:
                five_letter_word_freqs[row[0]] = int(row[1])

    five_letter_words = []
    with open("words_alpha.txt") as words_file:
        lines = words_file.readlines()
        for word in lines:
            word = word.rstrip()
            if len(word) == 5:
                five_letter_words.append(word)

    word_list = []
    for w in five_letter_words:
        word_list.append((w, five_letter_word_freqs.get(w, 0)))
    word_list.sort(key=lambda x: -x[1])
    return word_list


def read_wordle_raw(wordle_raw):
    res = []
    for row in wordle_raw:
        clean_row = []
        for char in row.split(" "):
            clean_row.append((char[0].lower(), char[1].lower()))
        res.append(clean_row)
    return res


def solve_wordle(wordle_raw):
    all_words = get_word_list()
    wordle_board = read_wordle_raw(wordle_raw)

    # priority 1: if any letters are green, filter out those words first
    char_definitely_at = {}
    char_not_at = {}
    char_not_in_word = set()
    for row in wordle_board:
        if len(row) != 5:
            raise Exception("Row is not 5 characters long")
        for i in range(len(row)):
            char, color = row[i]
            if color == "g":
                char_definitely_at[char] = i
            elif color == "y":
                lst = char_not_at.get(char, [])
                lst.append(i)
                char_not_at[char] = lst
            elif color == "b":
                char_not_in_word.add(char)
            else:
                raise Exception("Invalid color")

    remaining_after_greens = []
    for (w, f) in all_words:
        passed = True
        for char in char_definitely_at:
            idx = char_definitely_at[char]
            if w[idx] != char:
                passed = False
                break
        if not passed:
            continue
        remaining_after_greens.append((w, f))

    remaining_after_yellows = []
    for (w, f) in remaining_after_greens:
        missing_char = False
        for char in char_not_at:
            if char not in w:
                missing_char = True

        char_in_wrong_place = False
        for i in range(len(w)):
            char = w[i]
            if i in char_not_at.get(char, []):
                char_in_wrong_place = True
        if missing_char or char_in_wrong_place:
            continue
        remaining_after_yellows.append((w, f))

    remaining_after_blacks = []
    for (w, f) in remaining_after_yellows:
        passed = True
        for c in w:
            if c in char_not_in_word and c not in char_not_at:
                passed = False
                break
        if passed:
            remaining_after_blacks.append((w, f))

    print("Recommended next guesses: \n")
    for (word, freq) in remaining_after_blacks[:10]:
        print(" - " + word + " " + str(freq))


"""
Replace content here with your wordle board

Recommended starting worde: CRANE

Format: Upper case letter (A-Z), lower case color (byg)
"""
wordle_raw = [
    "Cb Rb Ay Nb Ey",
    "Vb Ay Ly Ub Ey",
]
solve_wordle(wordle_raw)
