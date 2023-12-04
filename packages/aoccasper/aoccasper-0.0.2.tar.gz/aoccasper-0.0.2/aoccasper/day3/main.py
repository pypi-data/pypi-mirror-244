from collections import defaultdict
from typing import NamedTuple

from aoccasper.utils import autoinput, split_input

NumberInfo = NamedTuple("NumberInfo", number=int, x_start=int, x_end=int, y=int)
GearInfo = NamedTuple("GearInfo", x=int, y=int)


def _retreive_number_infos(strings: list[str]):
    number_infos = []
    for i_row, row in enumerate(strings):
        start_idx, in_number = 0, False
        for i_col, col in enumerate(row):
            if col.isnumeric():
                if not in_number:
                    in_number = True
                    start_idx = i_col
            else:
                if in_number:
                    number_infos.append(NumberInfo(int(row[start_idx:i_col]), start_idx, i_col, i_row))
                    in_number = False
        if in_number:
            number_infos.append(NumberInfo(int(row[start_idx:len(row)]), start_idx, len(row), i_row))
    return number_infos


@autoinput(2023, 3)
@split_input
def part_1(inp):
    number_infos = _retreive_number_infos(inp)
    grid_info = [inp_it.replace(".", "0") for inp_it in inp]
    numbers_sum = 0
    X, Y = len(inp[0]), len(inp)
    for number_info in number_infos:
        x_a, x_b = max(number_info.x_start - 1, 0), min(number_info.x_end + 1, X)
        y_a, y_b = max(number_info.y - 1, 0), min(number_info.y + 2, Y)
        chars = ""
        for y in range(y_a, y_b):
            chars += grid_info[y][x_a:x_b]
        if not chars.isnumeric():
            numbers_sum += number_info.number
    return numbers_sum


@autoinput(2023, 3)
@split_input
def part_2(inp):
    number_infos = _retreive_number_infos(inp)
    grid_info = [inp_it.replace(".", "0") for inp_it in inp]
    gear_registry: dict[GearInfo, list[NumberInfo]] = defaultdict(list)
    X, Y = len(inp[0]), len(inp)
    for number_info in number_infos:
        x_a, x_b = max(number_info.x_start - 1, 0), min(number_info.x_end + 1, X)
        y_a, y_b = max(number_info.y - 1, 0), min(number_info.y + 2, Y)
        for y in range(y_a, y_b):
            for x in range(x_a, x_b):
                if not grid_info[y][x].isnumeric():
                    gear_registry[GearInfo(x, y)].append(number_info)

    product_sums = 0
    for gear in gear_registry:
        if len(gear_registry[gear]) == 2:
            product_sums += gear_registry[gear][0].number * gear_registry[gear][1].number

    return product_sums


if __name__ == "__main__":
    test_input_1 = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    p1 = part_1(test_input_1)
    test_input_2 = test_input_1
    p2 = part_2(test_input_2)

