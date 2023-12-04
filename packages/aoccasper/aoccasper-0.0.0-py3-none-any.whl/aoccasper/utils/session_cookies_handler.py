_mem = {"session_cookies": None}


def _set_session_cookies(session_cookies):
    _mem["session_cookies"] = session_cookies


def _get_session_cookies():
    return _mem["session_cookies"]
