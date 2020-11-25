import unittest

from onlinejudge_api.main import main


class DownloadAtCoderTest(unittest.TestCase):
    def test_icpc2013spring_a(self):
        """This problem contains both words `Input` and `Output` for the headings for sample outputs.
        """

        url = 'http://jag2013spring.contest.atcoder.jp/tasks/icpc2013spring_a'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://atcoder.jp/contests/jag2013spring/tasks/icpc2013spring_a",
                "tests": [{
                    "input": "2 2\n2 \n1 >= 3\n2 <= 5\n2\n1 >= 4\n2 >= 3\n",
                    "output": "Yes\n"
                }, {
                    "input": "2 2\n2 \n1 >= 5\n2 >= 5\n2\n1 <= 4\n2 <= 3\n",
                    "output": "Yes\n"
                }, {
                    "input": "2 2\n2 \n1 >= 3\n2 <= 3\n2\n1 <= 2\n2 >= 5\n",
                    "output": "No\n"
                }, {
                    "input": "1 2\n2\n1 <= 10\n1 >= 15\n",
                    "output": "No\n"
                }, {
                    "input": "5 5\n3\n2 <= 1\n3 <= 1\n4 <= 1\n4\n2 >= 2\n3 <= 1\n4 <= 1\n5 <= 1\n3\n3 >= 2\n4 <= 1\n5 <= 1\n2\n4 >= 2\n5 <= 1\n1\n5 >= 2 \n",
                    "output": "Yes\n"
                }],
                "name": "Everlasting Zero",
                "context": {
                    "contest": {
                        "name": "Japan Alumni Group Spring Contest 2013",
                        "url": "https://atcoder.jp/contests/jag2013spring"
                    },
                    "alphabet": "A"
                },
                "memoryLimit": 128,
                "timeLimit": 5000
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_arc035_a(self):
        """This problem uses <code> tags in the descriptoin text in the sample section.
        """

        url = 'http://arc035.contest.atcoder.jp/tasks/arc035_a'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://atcoder.jp/contests/arc035/tasks/arc035_a",
                "tests": [{
                    "input": "ab*\n",
                    "output": "YES\n"
                }, {
                    "input": "abc\n",
                    "output": "NO\n"
                }, {
                    "input": "a*bc*\n",
                    "output": "YES\n"
                }, {
                    "input": "***\n",
                    "output": "YES\n"
                }],
                "name": "\u9ad8\u6a4b\u304f\u3093\u3068\u56de\u6587",
                "context": {
                    "contest": {
                        "name": "AtCoder Regular Contest 035",
                        "url": "https://atcoder.jp/contests/arc035"
                    },
                    "alphabet": "A"
                },
                "memoryLimit": 256,
                "timeLimit": 2000
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_abc114_c(self):
        """This tests a problem which uses a new-style format HTML.
        """

        url = 'https://atcoder.jp/contests/abc114/tasks/abc114_c'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://atcoder.jp/contests/abc114/tasks/abc114_c",
                "tests": [{
                    "input": "575\n",
                    "output": "4\n"
                }, {
                    "input": "3600\n",
                    "output": "13\n"
                }, {
                    "input": "999999999\n",
                    "output": "26484\n"
                }],
                "name": "755",
                "context": {
                    "contest": {
                        "name": "AtCoder Beginner Contest 114",
                        "url": "https://atcoder.jp/contests/abc114"
                    },
                    "alphabet": "C"
                },
                "memoryLimit": 1024,
                "timeLimit": 2000
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_call_download_atcoder_abc003_4(self):
        """This tests a problem which uses an old-style format HTML.
        """

        url = 'https://atcoder.jp/contests/abc003/tasks/abc003_4'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://atcoder.jp/contests/abc003/tasks/abc003_4",
                "tests": [{
                    "input": "3 2\n2 2\n2 2\n",
                    "output": "12\n"
                }, {
                    "input": "4 5\n3 1\n3 0\n",
                    "output": "10\n"
                }, {
                    "input": "23 18\n15 13\n100 95\n",
                    "output": "364527243\n"
                }, {
                    "input": "30 30\n24 22\n145 132\n",
                    "output": "976668549\n"
                }],
                "name": "AtCoder\u793e\u306e\u51ac",
                "context": {
                    "contest": {
                        "name": "AtCoder Beginner Contest 003",
                        "url": "https://atcoder.jp/contests/abc003"
                    },
                    "alphabet": "D"
                },
                "memoryLimit": 64,
                "timeLimit": 2000
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_agc036_b(self):
        """In this problem, a sample output is empty.
        """

        url = 'https://atcoder.jp/contests/agc036/tasks/agc036_b'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://atcoder.jp/contests/agc036/tasks/agc036_b",
                "tests": [{
                    "input": "3 2\n1 2 3\n",
                    "output": "2 3\n"
                }, {
                    "input": "5 10\n1 2 3 2 3\n",
                    "output": "3\n"
                }, {
                    "input": "6 1000000000000\n1 1 2 2 3 3\n",
                    "output": "\n"
                }, {
                    "input": "11 97\n3 1 4 1 5 9 2 6 5 3 5\n",
                    "output": "9 2 6\n"
                }],
                "name": "Do Not Duplicate",
                "context": {
                    "contest": {
                        "name": "AtCoder Grand Contest 036",
                        "url": "https://atcoder.jp/contests/agc036"
                    },
                    "alphabet": "B"
                },
                "memoryLimit": 1024,
                "timeLimit": 2000
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_tenka1_2014_quala_e(self):
        """This problem uses an unusual HTML markup.

        .. seealso::
            https://github.com/kmyk/online-judge-tools/issues/618
        """

        url = 'https://atcoder.jp/contests/tenka1-2014-quala/tasks/tenka1_2014_qualA_e'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://atcoder.jp/contests/tenka1-2014-quala/tasks/tenka1_2014_qualA_e",
                "tests": [{
                    "input": "5 3\nAAB\nABB\nCDE\nFFH\nGHH\n2\n1 1\n2 3\n",
                    "output": "15\n7\n"
                }, {
                    "input": "2 2\nAB\nBA\n2\n1 1\n2 1\n",
                    "output": "2\n2\n"
                }, {
                    "input": "5 5\nAABAA\nACDEA\nAFGHA\nAIJKA\nAAAAA\n1\n3 1\n",
                    "output": "25\n"
                }],
                "name": "\u30d1\u30ba\u30eb\u306e\u79fb\u52d5",
                "context": {
                    "contest": {
                        "name": "\u5929\u4e0b\u4e00\u30d7\u30ed\u30b0\u30e9\u30de\u30fc\u30b3\u30f3\u30c6\u30b9\u30c82014\u4e88\u9078A",
                        "url": "https://atcoder.jp/contests/tenka1-2014-quala"
                    },
                    "alphabet": "E"
                },
                "memoryLimit": 256,
                "timeLimit": 5000
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_non_existing_problem(self):
        """This tests an non-existing problem.
        """

        url = 'http://abc001.contest.atcoder.jp/tasks/abc001_100'
        expected = {
            "status": "error",
            "messages": ["requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://atcoder.jp/contests/abc001/tasks/abc001_100"],
            "result": None,
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_impossible_problem(self):
        """This tests a problem impossible to parse sample cases.
        """

        url = 'https://chokudai001.contest.atcoder.jp/tasks/chokudai_001_a'
        expected = {
            "status": "error",
            "messages": ["onlinejudge.type.SampleParseError: failed to parse samples"],
            "result": None,
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)
