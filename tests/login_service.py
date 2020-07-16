import contextlib
import os
import pathlib
import tempfile
import unittest
from typing import *

from onlinejudge_api.main import main

ATCODER_USERNAME = 'ATCODER_USERNAME'
ATCODER_PASSWORD = 'ATCODER_PASSWORD'
CODEFORCES_USERNAME = 'CODEFORCES_USERNAME'
CODEFORCES_PASSWORD = 'CODEFORCES_PASSWORD'


@contextlib.contextmanager
def update_environ(**kwargs) -> Iterator[None]:
    preserved = dict(os.environ)
    os.environ.update(kwargs)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(preserved)


@contextlib.contextmanager
def temporary_cookie() -> Iterator[pathlib.Path]:
    with tempfile.TemporaryDirectory() as tempdir:
        yield pathlib.Path(tempdir) / 'cookie.jar'


class LoginServiceAtCoderTest(unittest.TestCase):
    """This tests the feature to logging in to AtCoder

    The user for test is: https://atcoder.jp/users/onlinejudgetools
    """
    @unittest.skipIf(not (ATCODER_USERNAME in os.environ and ATCODER_PASSWORD in os.environ), 'credentails for AtCoder is required')
    def test_login_success(self) -> None:
        url = 'https://atcoder.jp/'
        expected = {"status": "ok", "messages": [], "result": {"loggedIn": True}}

        with update_environ(USERNAME=os.environ[ATCODER_USERNAME], PASSWORD=os.environ[ATCODER_PASSWORD]):
            with temporary_cookie() as cookie_path:
                actual = main(['--cookie', str(cookie_path), 'login-service', url], debug=True)
        self.assertEqual(expected, actual)

    def test_login_failure(self) -> None:
        url = 'https://atcoder.jp/'
        expected = {"status": "error", "messages": ["onlinejudge.type.LoginError: failed to login"], "result": None}

        with update_environ(USERNAME='onlinejudgetools', PASSWORD='password'):
            with temporary_cookie() as cookie_path:
                actual = main(['--cookie', str(cookie_path), 'login-service', url], debug=True)
        self.assertEqual(expected, actual)


class LoginServiceCodeforcesTest(unittest.TestCase):
    """This tests the feature to logging in to Codeforces

    The user for test is: https://codeforces.com/profile/online-judge-tools
    """
    @unittest.skipIf(not (CODEFORCES_USERNAME in os.environ and CODEFORCES_PASSWORD in os.environ), 'credentails for Codeforces is required')
    def test_login_success(self) -> None:
        url = 'https://codeforces.com/'
        expected = {"status": "ok", "messages": [], "result": {"loggedIn": True}}

        with update_environ(USERNAME=os.environ[CODEFORCES_USERNAME], PASSWORD=os.environ[CODEFORCES_PASSWORD]):
            with temporary_cookie() as cookie_path:
                actual = main(['--cookie', str(cookie_path), 'login-service', url], debug=True)
        self.assertEqual(expected, actual)

    def test_login_failure(self) -> None:
        url = 'https://codeforces.com/'
        expected = {'status': 'error', 'messages': ['onlinejudge.type.LoginError: Invalid handle or password.'], 'result': None}

        with update_environ(USERNAME='online-judge-tools', PASSWORD='password'):
            with temporary_cookie() as cookie_path:
                actual = main(['--cookie', str(cookie_path), 'login-service', url], debug=True)
        self.assertEqual(expected, actual)
