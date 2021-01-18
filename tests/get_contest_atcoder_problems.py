import unittest

from onlinejudge_api.main import main


class GetContestAtCoderProblemsTest(unittest.TestCase):
    def test_21fb8ee5(self):
        url = 'https://kenkoooo.com/atcoder/#/contest/show/21fb8ee5-c293-4c5b-8d3d-9169afdf6fcf'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://kenkoooo.com/atcoder/#/contest/show/21fb8ee5-c293-4c5b-8d3d-9169afdf6fcf",
                "name": "\u3042\u3055\u304b\u306411/19",
                "problems": [
                    {
                        "url": "https://atcoder.jp/contests/abc164/tasks/abc164_c",
                        "name": "C. gacha",
                        "context": {
                            "contest": {
                                "url": "https://kenkoooo.com/atcoder/#/contest/show/21fb8ee5-c293-4c5b-8d3d-9169afdf6fcf",
                                "name": "\u3042\u3055\u304b\u306411/19"
                            },
                            "alphabet": "0"
                        }
                    },
                    {
                        "url": "https://atcoder.jp/contests/tenka1-2014-quala/tasks/tenka1_2014_qualA_a",
                        "name": "A. \u5929\u4e0b\u4e00\u5e8f\u6570",
                        "context": {
                            "contest": {
                                "url": "https://kenkoooo.com/atcoder/#/contest/show/21fb8ee5-c293-4c5b-8d3d-9169afdf6fcf",
                                "name": "\u3042\u3055\u304b\u306411/19"
                            },
                            "alphabet": "1"
                        }
                    },
                    {
                        "url": "https://atcoder.jp/contests/arc073/tasks/arc073_a",
                        "name": "C. Sentou",
                        "context": {
                            "contest": {
                                "url": "https://kenkoooo.com/atcoder/#/contest/show/21fb8ee5-c293-4c5b-8d3d-9169afdf6fcf",
                                "name": "\u3042\u3055\u304b\u306411/19"
                            },
                            "alphabet": "2"
                        }
                    },
                    {
                        "url": "https://atcoder.jp/contests/abc140/tasks/abc140_d",
                        "name": "D. Face Produces Unhappiness",
                        "context": {
                            "contest": {
                                "url": "https://kenkoooo.com/atcoder/#/contest/show/21fb8ee5-c293-4c5b-8d3d-9169afdf6fcf",
                                "name": "\u3042\u3055\u304b\u306411/19"
                            },
                            "alphabet": "3"
                        }
                    },
                    {
                        "url": "https://atcoder.jp/contests/arc074/tasks/arc074_a",
                        "name": "C. Chocolate Bar",
                        "context": {
                            "contest": {
                                "url": "https://kenkoooo.com/atcoder/#/contest/show/21fb8ee5-c293-4c5b-8d3d-9169afdf6fcf",
                                "name": "\u3042\u3055\u304b\u306411/19"
                            },
                            "alphabet": "4"
                        }
                    },
                    {
                        "url": "https://atcoder.jp/contests/agc026/tasks/agc026_c",
                        "name": "C. String Coloring",
                        "context": {
                            "contest": {
                                "url": "https://kenkoooo.com/atcoder/#/contest/show/21fb8ee5-c293-4c5b-8d3d-9169afdf6fcf",
                                "name": "\u3042\u3055\u304b\u306411/19"
                            },
                            "alphabet": "5"
                        }
                    },
                ]
            },
        }
        actual = main(['get-contest', url], debug=True)
        self.assertEqual(expected, actual)
