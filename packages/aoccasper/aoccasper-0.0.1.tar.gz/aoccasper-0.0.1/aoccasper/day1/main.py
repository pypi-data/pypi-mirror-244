from aoccasper.utils import autoinput, split_input


_WORD_NUMBER_DICT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def _find_first_and_last_number(string: str):
    first_number = int(next(filter(lambda x: x.isnumeric(), string)))
    last_number = int(next(filter(lambda x: x.isnumeric(), reversed(string))))
    return (first_number * 10) + last_number


def _fancy_replace_word_with_number(string: str):
    for word, number in _WORD_NUMBER_DICT.items():
        idx = string.find(word)
        if idx != -1:
            string = string[:idx+1] + str(number) + string[idx+2:]
        idx = string.rfind(word)
        if idx != -1:
            string = string[:idx + 1] + str(number) + string[idx + 2:]
    return string


@autoinput(2023, 1)
@split_input
def part_1(inp):
    base_number = 0
    for line in inp:
        base_number += _find_first_and_last_number(line)
    return base_number


@autoinput(2023, 1)
@split_input
def part_2(inp):
    base_number = 0
    for line in inp:
        line = _fancy_replace_word_with_number(line)
        base_number += _find_first_and_last_number(line)
    return base_number


if __name__ == "__main__":
    test_input_1 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
    p1 = part_1(test_input_1)
    test_input_2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    p2 = part_2(test_input_2)

