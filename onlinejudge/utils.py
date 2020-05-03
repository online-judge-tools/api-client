# Python Version: 3.x
"""
the module for those who make programs using online-judge-tools as a library
"""

import contextlib
import http
import pathlib
from typing import *

import appdirs

import onlinejudge._implementation.logging as log
from onlinejudge.type import *

user_data_dir = pathlib.Path(appdirs.user_data_dir('online-judge-tools'))
user_cache_dir = pathlib.Path(appdirs.user_cache_dir('online-judge-tools'))

_default_session = None  # Optional[requests.Session]


# NOTE: this function should not be used internally; if used, we may make bugs that given sessions are ignored
def get_default_session() -> requests.Session:
    """
    get the default session used in online-judge-tools

    :note: cookie is not saved to disk by default. check :py:func:`with_cookiejar`
    :note: the user agent is the default of the requests library.
    """

    global _default_session
    if _default_session is None:
        _default_session = requests.session()
    return _default_session


default_cookie_path = user_data_dir / 'cookie.jar'


@contextlib.contextmanager
def with_cookiejar(session: requests.Session, *, path: pathlib.Path = default_cookie_path) -> Iterator[requests.Session]:
    """

    :param session: the session to set a cookiejar
    :param path: a path to the file to store cookies. the default cookiejar is used if :py:class:`None`
    """

    session.cookies = http.cookiejar.LWPCookieJar(str(path))  # type: ignore
    if path.exists():
        log.status('load cookie from: %s', path)
        session.cookies.load()  # type: ignore
    yield session
    log.status('save cookie to: %s', path)
    path.parent.mkdir(parents=True, exist_ok=True)
    session.cookies.save()  # type: ignore
    path.chmod(0o600)  # NOTE: to make secure a little bit
