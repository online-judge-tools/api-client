import unittest

from onlinejudge_api.main import main


class GetContestCodeChefTest(unittest.TestCase):
    def test_cook131b(self):
        url = "https://www.codechef.com/COOK131B"
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://www.codechef.com/COOK131B",
                "problems": [{
                    "url": "https://www.codechef.com/COOK131B/problems/SHOEFIT",
                    "name": "Shoe Fit",
                    "context": {
                        "contest": {
                            "name": "July Cook-Off 2021 Division 2",
                            "url": "https://www.codechef.com/COOK131B"
                        }
                    }
                }, {
                    "url": "https://www.codechef.com/COOK131B/problems/CHFGCD",
                    "name": "Chef and GCD",
                    "context": {
                        "contest": {
                            "name": "July Cook-Off 2021 Division 2",
                            "url": "https://www.codechef.com/COOK131B"
                        }
                    }
                }, {
                    "url": "https://www.codechef.com/COOK131B/problems/XORORED",
                    "name": "XOR-ORED",
                    "context": {
                        "contest": {
                            "name": "July Cook-Off 2021 Division 2",
                            "url": "https://www.codechef.com/COOK131B"
                        }
                    }
                }, {
                    "url": "https://www.codechef.com/COOK131B/problems/CHFPLN",
                    "name": "Chef In Infinite Plane",
                    "context": {
                        "contest": {
                            "name": "July Cook-Off 2021 Division 2",
                            "url": "https://www.codechef.com/COOK131B"
                        }
                    }
                }, {
                    "url": "https://www.codechef.com/COOK131B/problems/MODEQUAL",
                    "name": "Mod Equality",
                    "context": {
                        "contest": {
                            "name": "July Cook-Off 2021 Division 2",
                            "url": "https://www.codechef.com/COOK131B"
                        }
                    }
                }, {
                    "url": "https://www.codechef.com/COOK131B/problems/BEAUSUB",
                    "name": "Beautiful Subsequence",
                    "context": {
                        "contest": {
                            "name": "July Cook-Off 2021 Division 2",
                            "url": "https://www.codechef.com/COOK131B"
                        }
                    }
                }, {
                    "url": "https://www.codechef.com/COOK131B/problems/COLRGRPH",
                    "name": "Hidden Colored Graph",
                    "context": {
                        "contest": {
                            "name": "July Cook-Off 2021 Division 2",
                            "url": "https://www.codechef.com/COOK131B"
                        }
                    }
                }, {
                    "url": "https://www.codechef.com/COOK131B/problems/MATBEAUT",
                    "name": "Make the Matrix Beautiful",
                    "context": {
                        "contest": {
                            "name": "July Cook-Off 2021 Division 2",
                            "url": "https://www.codechef.com/COOK131B"
                        }
                    }
                }, {
                    "url": "https://www.codechef.com/COOK131B/problems/SPTREE2",
                    "name": "A Special Tree 2",
                    "context": {
                        "contest": {
                            "name": "July Cook-Off 2021 Division 2",
                            "url": "https://www.codechef.com/COOK131B"
                        }
                    }
                }, {
                    "url": "https://www.codechef.com/COOK131B/problems/GCDLEN",
                    "name": "Maximal GCD",
                    "context": {
                        "contest": {
                            "name": "July Cook-Off 2021 Division 2",
                            "url": "https://www.codechef.com/COOK131B"
                        }
                    }
                }],
                "name": "July Cook-Off 2021 Division 2"
            },
        }
        actual = main(['get-contest', url], debug=True)
        self.assertEqual(expected, actual)
