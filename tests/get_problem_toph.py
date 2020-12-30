import unittest

from onlinejudge_api.main import main


class GetProblemTophTest(unittest.TestCase):
    def test_new_year_couple(self) -> None:
        url = 'https://toph.co/p/new-year-couple'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://toph.co/p/new-year-couple",
                "tests": [
                    {
                        "input": "8\r\nmrtarek 10 20\r\noptarkk 15 30\r\nmmtarqq 12 25\r\naatarcc 8 18\r\nheloptr 22 50\r\nmemopto 10 40\r\nkokoptz 15 45\r\nlmkoopa 5 90\r\n5\r\n3 5 20\r\n3 5 11\r\n3 5 16\r\n5 6 25\r\n5 6 16",
                        "output": "3\r\n1\r\n6\r\n3\r\n1"
                    },
                    {
                        "input": "5\r\noookhzal 11 20\r\napkoptay 10 45\r\nappokyat 30 32\r\npopaozal 10 15\r\ntotkozal 15 25\r\n4\r\n6 8 15\r\n7 7 10\r\n3 5 25\r\n1 2 30",
                        "output": "3\r\n1\r\n0\r\n1\r\n"
                    },
                ],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_power_and_mod(self) -> None:
        url = 'https://toph.co/p/power-and-mod'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://toph.co/p/power-and-mod",
                "tests": [
                    {
                        "input": "2\r\n2 3 4\r\n3 4 5",
                        "output": "0\r\n1"
                    },
                ],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)
