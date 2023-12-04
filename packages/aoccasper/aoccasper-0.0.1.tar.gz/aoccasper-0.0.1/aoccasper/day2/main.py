from typing import NamedTuple

from aoccasper.utils import autoinput, split_input

BallFrequency = NamedTuple("BallFrequency", red=int, blue=int, green=int)
GameInfo = NamedTuple("GameInfo", game_id=int, game_data=tuple[BallFrequency])


_COLOR_ENUM = {
    "red": 0,
    "green": 1,
    "blue": 2,
}

_MAX_BALLS = (12, 13, 14)


def _int_or_enum(string: str):
    try:
        return int(string)
    except ValueError:
        return _COLOR_ENUM[string]


def _parse_input(strings: list[str]) -> tuple[GameInfo]:
    game_info = []
    for game in strings:
        game_str, rest_str = game.split(":")
        game_id = int(game_str.split(" ")[-1])
        showings_raw = rest_str.split(";")
        showings = [[item.strip() for item in showing.split(",")] for showing in showings_raw]
        encoded_showings = []
        for showing in showings:
            rgb_color_freqs = [0, 0, 0]
            for item in showing:
                freq, ball_color_index = map(_int_or_enum, item.split(" "))
                rgb_color_freqs[ball_color_index] = freq
            encoded_showings.append(BallFrequency(*rgb_color_freqs))
        game_info.append(GameInfo(game_id, tuple(encoded_showings)))
    return tuple(game_info)


@autoinput(2023, 2)
@split_input
def part_1(inp):
    game_infos = _parse_input(inp)
    game_id_sum = 0
    for game_info in game_infos:
        if all(
            all(balls_pulled <= balls_available for (balls_pulled, balls_available) in zip(showing, _MAX_BALLS))
            for showing in game_info.game_data
        ):
            game_id_sum += game_info.game_id
    return game_id_sum


@autoinput(2023, 2)
@split_input
def part_2(inp):
    game_infos = _parse_input(inp)
    game_power_sum = 0
    for game_info in game_infos:
        red_balls = max(bf.red for bf in game_info.game_data)
        green_balls = max(bf.green for bf in game_info.game_data)
        blue_balls = max(bf.blue for bf in game_info.game_data)

        game_power_sum += red_balls * green_balls * blue_balls
    return game_power_sum


if __name__ == "__main__":
    test_input_1 = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    # p1 = part_1(test_input_1)
    test_input_2 = test_input_1
    p2 = part_2(test_input_2)

