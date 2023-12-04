import functools
import requests

from aoccasper.utils import get_session_cookies


_DEFAULT_SESSION_COOKIES = "53616c7465645f5fbbb82f5ab127ccc91dfe7395682bf132e37f590f908165d33c9d831d5220c73e2163f69ebaf1206fda642b6cd0764676206d2c016dfe1960"


def split_input(func):
    @functools.wraps(func)
    def inner(inp):
        if isinstance(inp, str):
            inp = inp.split("\n")
        return func(inp)
    return inner


def autoinput(year, day, session_cookies=None):
    def decorator(func):
        functools.wraps(func)

        def inner(inp=None):
            if inp is None:
                resp = requests.get(f"https://adventofcode.com/{year}/day/{day}/input",
                                    cookies={"session": get_session_cookies() or _DEFAULT_SESSION_COOKIES})
                inp = resp.content.decode()[:-1]
            return func(inp)
        return inner
    return decorator
