import unittest

from onlinejudge_api.main import main


class GetProblemCodeforcesTest(unittest.TestCase):
    def test_problemset_700_b(self):
        url = 'http://codeforces.com/problemset/problem/700/B'
        expected = {"status": "ok", "messages": [], "result": {"url": "https://codeforces.com/problemset/problem/700/B", "tests": [{"input": "7 2\n1 5 6 2\n1 3\n3 2\n4 5\n3 7\n4 3\n4 6\n", "output": "6\n"}, {"input": "9 3\n3 2 1 6 5 9\n8 9\n3 2\n2 7\n3 4\n7 6\n4 5\n2 1\n2 8\n", "output": "9\n"}], "context": {}}}
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_contest_538_h(self):
        url = 'http://codeforces.com/contest/538/problem/H'
        expected = {"status": "ok", "messages": [], "result": {"url": "https://codeforces.com/contest/538/problem/H", "tests": [{"input": "10 20\n3 0\n3 6\n4 9\n16 25\n", "output": "POSSIBLE\n4 16\n112\n"}, {"input": "1 10\n3 3\n0 10\n0 10\n0 10\n1 2\n1 3\n2 3\n", "output": "IMPOSSIBLE\n"}], "name": "Summer Dichotomy", "context": {"contest": {"name": "Codeforces Round #300", "url": "https://codeforces.com/contest/538"}, "alphabet": "H"}}}
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_gym_101020_a(self):
        url = 'http://codeforces.com/gym/101020/problem/A'
        expected = {"status": "ok", "messages": [], "result": {"url": "https://codeforces.com/gym/101020/problem/A", "tests": [{"input": "3\n5 4\n1 2\n33 33\n", "output": "20\n2\n1089\n"}], "name": "Jerry's Window", "context": {"contest": {"name": "2015 Syrian Private Universities Collegiate Programming Contest", "url": "https://codeforces.com/gym/101020"}, "alphabet": "A"}}}
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_contest_1080_a(self):
        url = 'https://codeforces.com/contest/1080/problem/A'
        expected = {"status": "ok", "messages": [], "result": {"url": "https://codeforces.com/contest/1080/problem/A", "tests": [{"input": "3 5\n", "output": "10\n"}, {"input": "15 6\n", "output": "38\n"}], "name": "Petya and Origami", "context": {"contest": {"name": "Codeforces Round #524 (Div. 2)", "url": "https://codeforces.com/contest/1080"}, "alphabet": "A"}}}
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)
