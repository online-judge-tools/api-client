import unittest

from onlinejudge_api.main import main


class GetProblemHackerRankTest(unittest.TestCase):
    # TODO: support parsing HTML or retrieving from "Run Code" feature
    def test_hourrank_1_beautiful_array(self):
        """the "Download all test cases" feature is not supported for this problem.
        """

        url = 'https://www.hackerrank.com/contests/hourrank-1/challenges/beautiful-array'
        expected = {
            "status": "error",
            "messages": ["requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://www.hackerrank.com/rest/contests/hourrank-1/challenges/beautiful-array/download_testcases"],
            "result": None,
        }

        actual = main(['--user-agent', 'dummy', 'get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_hourrank_30_video_conference(self):
        url = 'https://www.hackerrank.com/contests/101hack54/challenges/weather-forecast-quality'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://www.hackerrank.com/contests/101hack54/challenges/weather-forecast-quality",
                "tests": [
                    {
                        "input": "14 13 12 13 16 18 21\n15 11 12 11 16 19 24\n",
                        "output": "9\n"
                    },
                    {
                        "input": "-73 48 -86 72 -16 96 29\n60 -96 67 -16 97 10 -60\n",
                        "output": "806\n"
                    },
                    {
                        "input": "48 69 -34 66 -43 49 31\n-45 22 -77 -81 -54 -75 28\n",
                        "output": "468\n"
                    },
                    {
                        "input": "-36 -50 -4 -38 -99 -100 -21\n30 -4 17 46 -38 -35 45\n",
                        "output": "409\n"
                    },
                    {
                        "input": "-73 77 79 -54 -67 24 21\n-61 66 -53 56 -67 -21 72\n",
                        "output": "361\n"
                    },
                    {
                        "input": "100 -50 -91 92 -65 -73 -38\n100 -50 -91 92 -65 -73 -38\n",
                        "output": "0\n"
                    },
                    {
                        "input": "-100 -100 100 100 100 100 -100\n100 100 -100 -100 -100 -100 100\n",
                        "output": "1400\n"
                    },
                ],
                "context": {}
            },
        }

        actual = main(['--user-agent', 'dummy', 'get-problem', url], debug=True)
        self.assertEqual(expected, actual)
