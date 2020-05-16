import unittest

from onlinejudge_api.main import main


class GetProblemTopcoderTest(unittest.TestCase):
    def test_10760(self):
        # `double` is used and one of values is a scientific form `1.0E50`.
        url = 'https://community.topcoder.com/stat?c=problem_statement&pm=10760'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://community.topcoder.com/stat?c=problem_statement&pm=10760",
                "tests": [{
                    "input": "2 5 8\n",
                    "output": "40.0\n"
                }, {
                    "input": "2 1.5 1.8\n",
                    "output": "3.3\n"
                }, {
                    "input": "3 8.26 7.54 3.2567\n",
                    "output": "202.82857868\n"
                }, {
                    "input": "4 1.5 1.7 1.6 1.5\n",
                    "output": "9.920000000000002\n"
                }, {
                    "input": "50 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10\n",
                    "output": "1.0E50\n"
                }],
                "name": "Nisoku"
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_11026(self):
        # `String[]` is used.
        # The type of the return value is a list.
        url = 'https://community.topcoder.com/stat?c=problem_statement&pm=11026'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://community.topcoder.com/stat?c=problem_statement&pm=11026",
                "tests": [{
                    "input": "1 00\n1 00\n1 58\n",
                    "output": "2 0.38461538461538464 0.6153846153846154\n"
                }, {
                    "input": "2 00 00\n2 00 00\n2 21 11\n",
                    "output": "2 0.5888888888888889 0.4111111111111111\n"
                }, {
                    "input": "3 0000 0000 0000\n3 2284 0966 9334\n3 1090 3942 4336\n",
                    "output": "\n{0.19685958571981937, 0.24397246802233483, 0.31496640865458775, 0.24420153760325805 }\n"
                }, {
                    "input": "5 01010110 00011000 00001000 10001010 10111110\n5 22218214 32244284 68402430 18140323 29043145\n5 87688689 36101317 69474068 29337374 87255881\n",
                    "output": "\n{0.11930766223754977, 0.14033271060661345, 0.0652282589028571, 0.14448118133046356, 0.1981894622733832, 0.10743462836879789, 0.16411823601857622, 0.06090786026175882 }\n"
                }, {
                    "input": "1 10\n1 00\n1 00\n",
                    "output": "2 1.0 0.0\n"
                }],
                "name": "RandomApple"
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)
