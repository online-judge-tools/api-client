import os
import unittest

from onlinejudge_api.main import main
from tests.login_service import temporary_cookie, update_environ

CODEFORCES_USERNAME = 'CODEFORCES_USERNAME'
CODEFORCES_PASSWORD = 'CODEFORCES_PASSWORD'


class GetProblemCodeforcesTest(unittest.TestCase):
    def test_problemset_700_b(self):
        """This tests a problem in the problemset.
        """

        url = 'http://codeforces.com/problemset/problem/700/B'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://codeforces.com/problemset/problem/700/B",
                "tests": [{
                    "input": "7 2\n1 5 6 2\n1 3\n3 2\n4 5\n3 7\n4 3\n4 6\n",
                    "output": "6\n"
                }, {
                    "input": "9 3\n3 2 1 6 5 9\n8 9\n3 2\n2 7\n3 4\n7 6\n4 5\n2 1\n2 8\n",
                    "output": "9\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_contest_538_h(self):
        """This tests a old problem.
        """

        url = 'http://codeforces.com/contest/538/problem/H'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://codeforces.com/contest/538/problem/H",
                "tests": [{
                    "input": "10 20\n3 0\n3 6\n4 9\n16 25\n",
                    "output": "POSSIBLE\n4 16\n112\n"
                }, {
                    "input": "1 10\n3 3\n0 10\n0 10\n0 10\n1 2\n1 3\n2 3\n",
                    "output": "IMPOSSIBLE\n"
                }],
                "name": "Summer Dichotomy",
                "context": {
                    "contest": {
                        "name": "Codeforces Round #300",
                        "url": "https://codeforces.com/contest/538"
                    },
                    "alphabet": "H"
                }
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_gym_101020_a(self):
        """This tests a problem in the gym.
        """

        url = 'http://codeforces.com/gym/101020/problem/A'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://codeforces.com/gym/101020/problem/A",
                "tests": [{
                    "input": "3\n5 4\n1 2\n33 33\n",
                    "output": "20\n2\n1089\n"
                }],
                "name": "Jerry's Window",
                "context": {
                    "contest": {
                        "name": "2015 Syrian Private Universities Collegiate Programming Contest",
                        "url": "https://codeforces.com/gym/101020"
                    },
                    "alphabet": "A"
                }
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_contest_1080_a(self):
        """Recent (Nov 2018) problems has leading spaces for sample cases. We should check that they are removed.

        .. seealso::
            https://github.com/online-judge-tools/oj/issues/198
        """

        url = 'https://codeforces.com/contest/1080/problem/A'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://codeforces.com/contest/1080/problem/A",
                "tests": [{
                    "input": "3 5\n",
                    "output": "10\n"
                }, {
                    "input": "15 6\n",
                    "output": "38\n"
                }],
                "name": "Petya and Origami",
                "context": {
                    "contest": {
                        "name": "Codeforces Round #524 (Div. 2)",
                        "url": "https://codeforces.com/contest/1080"
                    },
                    "alphabet": "A"
                }
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_contest_1344_d(self):
        """The sample output of this problem has superfluous whitespaces. We should check that they are removed.

        .. seealso::
            see https://github.com/online-judge-tools/api-client/issues/24
        """

        url = 'https://codeforces.com/contest/1334/problem/D'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://codeforces.com/contest/1334/problem/D",
                "tests": [{
                    "input": "3\n2 1 3\n3 3 6\n99995 9998900031 9998900031\n",
                    "output": "1 2 1\n1 3 2 3\n1\n"
                }],
                "name": "Minimum Euler Cycle",
                "context": {
                    "contest": {
                        "name": "Educational Codeforces Round 85 (Rated for Div. 2)",
                        "url": "https://codeforces.com/contest/1334"
                    },
                    "alphabet": "D"
                }
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    @unittest.skipIf(not (CODEFORCES_USERNAME in os.environ and CODEFORCES_PASSWORD in os.environ), 'credentails for Codeforces is required')
    def test_edu_2_2_1_a(self):
        """This tests an educational problem.

        Unlike other problems educational problems are only accessible if the user is logged in.
        The user for test is: https://codeforces.com/profile/online-judge-tools
        """

        login_url = 'https://codeforces.com/'
        with update_environ(USERNAME=os.environ[CODEFORCES_USERNAME], PASSWORD=os.environ[CODEFORCES_PASSWORD]):
            with temporary_cookie() as cookie_path:
                main(['--cookie', str(cookie_path), 'login-service', login_url], debug=True)

                url = 'https://codeforces.com/edu/course/2/lesson/2/1/practice/contest/269100/problem/A'
                expected = {
                    "status": "ok",
                    "messages": [],
                    "result": {
                        "url": "https://codeforces.com/edu/course/2/lesson/2/1/practice/contest/269100/problem/A",
                        "tests": [{
                            "input": "ababba\n",
                            "output": "6 5 0 2 4 1 3\n"
                        }, {
                            "input": "aaaa\n",
                            "output": "4 3 2 1 0\n"
                        }, {
                            "input": "ppppplppp\n",
                            "output": "9 5 8 4 7 3 6 2 1 0\n"
                        }, {
                            "input": "nn\n",
                            "output": "2 1 0\n"
                        }],
                        "context": {}
                    },
                }
                actual = main(['--cookie', str(cookie_path), 'get-problem', url], debug=True)
                self.assertEqual(expected, actual)
