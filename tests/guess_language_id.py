import pathlib
import tempfile
import unittest

import tests.utils
from onlinejudge_api.main import main


class GuessLanguageIdTest(unittest.TestCase):
    """This class has end-to-end tests of `guess-language-id` subcommand.
    """
    @unittest.skipIf(not tests.utils.is_logged_in('https://atcoder.jp/'), 'login is required')
    def test_atcoder(self):
        url = 'https://atcoder.jp/contests/agc045/tasks/agc045_a'
        name = 'main.py'
        code = 'print("hello world")'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                'description': 'Python (3.8.2)',
                'id': '4006',
                'context': {
                    'problem': {
                        'url': 'https://atcoder.jp/contests/agc045/tasks/agc045_a'
                    }
                },
            },
        }

        with tempfile.TemporaryDirectory() as tempdir:
            path = pathlib.Path(tempdir) / name
            with path.open('w') as fh:
                fh.write(code)
            actual = main(['guess-language-id', url, '--file', str(path)], debug=True)
        self.assertEqual(expected, actual)

    @unittest.skipIf(not tests.utils.is_logged_in('https://codeforces.com/'), 'login is required')
    def test_codeforces(self):
        url = 'https://codeforces.com/problemset/problem/700/B'
        name = 'main.cpp'
        code = 'int main() {}'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "id": "61",
                "description": "GNU G++17 9.2.0 (64 bit, msys 2)",
                "context": {
                    "problem": {
                        "url": "https://codeforces.com/problemset/problem/700/B"
                    }
                },
            },
        }

        with tempfile.TemporaryDirectory() as tempdir:
            path = pathlib.Path(tempdir) / name
            with path.open('w') as fh:
                fh.write(code)
            actual = main(['guess-language-id', url, '--file', str(path)], debug=True)
        self.assertEqual(expected, actual)
