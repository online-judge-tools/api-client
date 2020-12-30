import unittest

from onlinejudge_api.main import main


class GetProblemKattisTest(unittest.TestCase):
    def test_8queens(self) -> None:
        url = 'https://open.kattis.com/contests/asiasg15prelwarmup/problems/8queens'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://open.kattis.com/contests/asiasg15prelwarmup/problems/8queens",
                "tests": [
                    {
                        "input": "*.......\n..*.....\n....*...\n......*.\n.*......\n.......*\n.....*..\n...*....\n",
                        "output": "invalid\n"
                    },
                    {
                        "input": "*.......\n......*.\n....*...\n.......*\n.*......\n...*....\n.....*..\n..*.....\n",
                        "output": "valid\n"
                    },
                ],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_amazingadventures(self) -> None:
        """test_amazingadventures() tests a problem whose domain is not "open.kattis.com".
        """

        url = 'https://hanoi18.kattis.com/problems/amazingadventures'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://hanoi18.kattis.com/problems/amazingadventures",
                "tests": [
                    {
                        "input": "3 3\n1 1\n3 3\n2 1\n2 2\n\n3 4\n1 1\n3 4\n2 1\n1 2\n\n2 2\n2 1\n2 2\n1 2\n1 1\n\n0 0\n",
                        "output": "YES\nRRUULLD\nNO\nYES\nRD\n"
                    },
                ],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)
