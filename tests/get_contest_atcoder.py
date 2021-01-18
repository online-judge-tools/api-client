import unittest

from onlinejudge_api.main import main


class GetContestAtcoderTest(unittest.TestCase):
    def test_abc012(self):
        url = "https://atcoder.jp/contests/abc012"
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://atcoder.jp/contests/abc012",
                "problems": [
                    {
                        "url": "https://atcoder.jp/contests/abc012/tasks/abc012_1",
                        "name": "\u30b9\u30ef\u30c3\u30d7",
                        "context": {
                            "contest": {
                                "name": "AtCoder Beginner Contest 012",
                                "url": "https://atcoder.jp/contests/abc012"
                            },
                            "alphabet": "A"
                        }
                    },
                    {
                        "url": "https://atcoder.jp/contests/abc012/tasks/abc012_2",
                        "name": "\u5165\u6d74\u6642\u9593",
                        "context": {
                            "contest": {
                                "name": "AtCoder Beginner Contest 012",
                                "url": "https://atcoder.jp/contests/abc012"
                            },
                            "alphabet": "B"
                        }
                    },
                    {
                        "url": "https://atcoder.jp/contests/abc012/tasks/abc012_3",
                        "name": "\u4e5d\u4e5d\u8db3\u3057\u7b97",
                        "context": {
                            "contest": {
                                "name": "AtCoder Beginner Contest 012",
                                "url": "https://atcoder.jp/contests/abc012"
                            },
                            "alphabet": "C"
                        }
                    },
                    {
                        "url": "https://atcoder.jp/contests/abc012/tasks/abc012_4",
                        "name": "\u30d0\u30b9\u3068\u907f\u3051\u3089\u308c\u306a\u3044\u904b\u547d",
                        "context": {
                            "contest": {
                                "name": "AtCoder Beginner Contest 012",
                                "url": "https://atcoder.jp/contests/abc012"
                            },
                            "alphabet": "D"
                        }
                    },
                ],
                "name": "AtCoder Beginner Contest 012"
            },
        }
        actual = main(['get-contest', url], debug=True)
        self.assertEqual(expected, actual)
