import unittest

from onlinejudge_api.main import main


class DownloadFacebookHackerCupTest(unittest.TestCase):
    def test_2020_qual_d1(self):
        url = 'https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/D1'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/D1",
                "tests": [{
                    "input": "7\n5 3\n0\n20\n30\n0\n10\n5 2\n0\n20\n30\n0\n10\n5 1\n0\n20\n30\n0\n10\n4 1\n99\n88\n77\n66\n4 4\n99\n88\n77\n66\n6 2\n0\n0\n20\n30\n0\n10\n12 3\n0\n1\n4\n7\n0\n5\n9\n8\n0\n3\n0\n6\n",
                    "output": "Case #1: 20\nCase #2: 30\nCase #3: -1\nCase #4: 165\nCase #5: 0\nCase #6: 50\nCase #7: 19\n"
                }],
                "context": {},
            },
        }
        actual = main(['--user-agent', 'dummy', 'get-problem', url], debug=True)
        self.assertEqual(expected, actual)
