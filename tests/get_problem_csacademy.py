import unittest

from onlinejudge_api.main import main


class GetProblemCSAcademyTest(unittest.TestCase):
    def test_k_swap(self) -> None:
        url = 'https://csacademy.com/contest/round-39/task/k-swap/'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://csacademy.com/contest/round-39/task/k-swap/",
                "tests": [
                    {
                        "input": "4 2\n4 3 2 1\n",
                        "output": "2 3 4 1 "
                    },
                    {
                        "input": "7 2\n4 3 2 1 2 3 4\n",
                        "output": "2 2 3 3 4 1 4 "
                    },
                    {
                        "input": "10 2\n4 3 2 1 2 3 4 3 2 1\n",
                        "output": "2 2 2 3 3 3 4 1 4 1 "
                    },
                ],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_unfair_game(self) -> None:
        url = 'https://csacademy.com/contest/archive/task/unfair_game/'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://csacademy.com/contest/archive/task/unfair_game/",
                "tests": [
                    {
                        "input": "5\n-1 2 10 -10 3\n",
                        "output": "14\n"
                    },
                    {
                        "input": "5\n-5 2 -10 4 -7\n",
                        "output": "-1\n"
                    },
                ],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)
