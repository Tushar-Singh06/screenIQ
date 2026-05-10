import re


WORD_TO_NUMBER = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}


def normalize_score(score):
    if isinstance(score, (int, float)):
        return float(score)

    score = str(score).strip().lower()

    if score in WORD_TO_NUMBER:
        return float(WORD_TO_NUMBER[score])

    match = re.search(r"\d+(\.\d+)?", score)

    if match:
        return float(match.group())

    return 0.0