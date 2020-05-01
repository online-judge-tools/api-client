import unittest

from onlinejudge_api.main import main


class GetProblemPOJTest(unittest.TestCase):
    def test_1000(self):
        url = 'http://poj.org/problem?id=1000'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://poj.org/problem?id=1000",
                "tests": [{
                    "input": "1 2\r\n",
                    "output": "3\r\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_2104(self):
        url = 'http://poj.org/problem?id=2104'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://poj.org/problem?id=2104",
                "tests": [{
                    "input": "7 3\r\n1 5 2 6 3 7 4\r\n2 5 3\r\n4 4 1\r\n1 7 3\r\n",
                    "output": "5\r\n6\r\n3\r\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_3150(self):
        url = 'http://poj.org/problem?id=3150'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://poj.org/problem?id=3150",
                "tests": [{
                    "input": "5 3 1 1\r\n1 2 2 1 2\r\n",
                    "output": "2 2 2 2 1\r\n"
                }, {
                    "input": "5 3 1 10\r\n1 2 2 1 2\r\n",
                    "output": "2 0 0 2 2\r\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)
