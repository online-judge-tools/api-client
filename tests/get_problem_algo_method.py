import unittest

from onlinejudge_api.main import main


class GetProblemAlgoMethodTest(unittest.TestCase):
    def test_tasks_22(self):
        url = 'https://algo-method.com/tasks/22'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://algo-method.com/tasks/22",
                "tests": [
                    {
                        "input": "power\n",
                        "output": "w\n"
                    },
                    {
                        "input": "otter\n",
                        "output": "t\n"
                    },
                ],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_tasks_24(self):
        url = 'https://algo-method.com/tasks/24'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://algo-method.com/tasks/24",
                "tests": [{
                    "input": "1 2\n",
                    "output": "3\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_tasks_529(self):
        url = 'https://algo-method.com/tasks/529'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://algo-method.com/tasks/529",
                "tests": [{
                    "input": "7\n0 1 0 0 1 5\n",
                    "output": "0\n1\n2\n1\n1\n2\n3\n"
                }, {
                    "input": "7\n0 0 0 0 0 0\n",
                    "output": "0\n1\n1\n1\n1\n1\n1\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)
