import os
import unittest

from onlinejudge_api.main import main

DROPBOX_TOKEN = 'DROPBOX_TOKEN'


class GetProblemAtCoderTest(unittest.TestCase):
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

    @unittest.skipIf(DROPBOX_TOKEN not in os.environ, '$DROPBOX_TOKEN is required')
    def test_abc100_a_system(self):
        url = "https://atcoder.jp/contests/abc170/tasks/abc170_a"
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://atcoder.jp/contests/abc170/tasks/abc170_a",
                "tests": [{
                    "input": "0 2 3 4 5\n",
                    "output": "1\n",
                    "name": "sample_01.txt"
                }, {
                    "input": "1 2 0 4 5\n",
                    "output": "3\n",
                    "name": "sample_02.txt"
                }, {
                    "input": "1 0 3 4 5\n",
                    "output": "2\n",
                    "name": "testcase_01.txt"
                }, {
                    "input": "1 2 3 0 5\n",
                    "output": "4\n",
                    "name": "testcase_02.txt"
                }, {
                    "input": "1 2 3 4 0\n",
                    "output": "5\n",
                    "name": "testcase_03.txt"
                }],
                "name": "Five Variables",
                "context": {
                    "contest": {
                        "name": "AtCoder Beginner Contest 170",
                        "url": "https://atcoder.jp/contests/abc170"
                    },
                    "alphabet": "A"
                },
                "memoryLimit": 1024,
                "timeLimit": 2000
            },
        }
        actual = main(['get-problem', '--system', url], debug=True)
        self.assertEqual(expected, actual)

    @unittest.skipIf(DROPBOX_TOKEN not in os.environ, '$DROPBOX_TOKEN is required')
    def test_agc015_d_system(self):
        """This problem has many system cases.
        """

        url = "https://atcoder.jp/contests/agc015/tasks/agc015_d"
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://atcoder.jp/contests/agc015/tasks/agc015_d",
                "tests": [
                    {
                        "input": "291009339170240866\n674343695741145096\n",
                        "output": "715018014342221116\r\n",
                        "name": "01.txt"
                    },
                    {
                        "input": "863409905090580085\n1006578334790476645\n",
                        "output": "146677634804966166\r\n",
                        "name": "02.txt"
                    },
                    {
                        "input": "24078168236682609\n183030523989780344\n",
                        "output": "264152207915029135\r\n",
                        "name": "03.txt"
                    },
                    {
                        "input": "826400924695647849\n845214609583738565\n",
                        "output": "22537211990528814\r\n",
                        "name": "04.txt"
                    },
                    {
                        "input": "860561421744037105\n932099142220704557\n",
                        "output": "80317007460124190\r\n",
                        "name": "05.txt"
                    },
                    {
                        "input": "582699648877758119\n998204746423694718\n",
                        "output": "570221855729088857\r\n",
                        "name": "06.txt"
                    },
                    {
                        "input": "843032974347839473\n843032974778081233\n",
                        "output": "807186462\r\n",
                        "name": "07.txt"
                    },
                    {
                        "input": "713567919670617009\n713644541636474237\n",
                        "output": "111883779251279\r\n",
                        "name": "08.txt"
                    },
                    {
                        "input": "1092302156216197631\n1111082247365283889\n",
                        "output": "24590551371685377\r\n",
                        "name": "09.txt"
                    },
                    {
                        "input": "492062383113917722\n492062383113918270\n",
                        "output": "742\r\n",
                        "name": "10.txt"
                    },
                    {
                        "input": "1035374452930311753\n1035374452930311757\n",
                        "output": "7\r\n",
                        "name": "11.txt"
                    },
                    {
                        "input": "983929096383725280\n983929096383725311\n",
                        "output": "32\r\n",
                        "name": "12.txt"
                    },
                    {
                        "input": "763360136839299073\n765611936652984319\n",
                        "output": "2251799813685247\r\n",
                        "name": "13.txt"
                    },
                    {
                        "input": "69946535201660593\n69964127387705005\n",
                        "output": "35180883026255\r\n",
                        "name": "14.txt"
                    },
                    {
                        "input": "864691128455135231\n864691128455135232\n",
                        "output": "3\r\n",
                        "name": "15.txt"
                    },
                    {
                        "input": "995295517648879614\n995295517648879616\n",
                        "output": "5\r\n",
                        "name": "16.txt"
                    },
                    {
                        "input": "1068463647721987401\n1068463647721987405\n",
                        "output": "7\r\n",
                        "name": "17.txt"
                    },
                    {
                        "input": "1141225601506803711\n1141225601506803712\n",
                        "output": "3\r\n",
                        "name": "18.txt"
                    },
                    {
                        "input": "739259304881709048\n739294026330537986\n",
                        "output": "69442897657876\r\n",
                        "name": "19.txt"
                    },
                    {
                        "input": "983181882147887497\n983181882147888817\n",
                        "output": "1655\r\n",
                        "name": "20.txt"
                    },
                    {
                        "input": "887974750935126937\n887974810959549283\n",
                        "output": "113313175758\r\n",
                        "name": "21.txt"
                    },
                    {
                        "input": "185470715875567418\n185470715877654644\n",
                        "output": "4174348\r\n",
                        "name": "22.txt"
                    },
                    {
                        "input": "675680155728273089\n675680156265144057\n",
                        "output": "805904703\r\n",
                        "name": "23.txt"
                    },
                    {
                        "input": "1134006168159047386\n1134006168159047387\n",
                        "output": "2\r\n",
                        "name": "24.txt"
                    },
                    {
                        "input": "138485029847246853\n138485029847246859\n",
                        "output": "10\r\n",
                        "name": "25.txt"
                    },
                    {
                        "input": "342868187160174261\n342868187164368561\n",
                        "output": "5390998\r\n",
                        "name": "26.txt"
                    },
                    {
                        "input": "1\n1152921504606846975\n",
                        "output": "1152921504606846975\r\n",
                        "name": "27.txt"
                    },
                    {
                        "input": "3\n1152921504606846975\n",
                        "output": "1152921504606846973\r\n",
                        "name": "28.txt"
                    },
                    {
                        "input": "743164597401505787\n743164600052172887\n",
                        "output": "4906901514\r\n",
                        "name": "29.txt"
                    },
                    {
                        "input": "466213636663985004\n466213636663985004\n",
                        "output": "1\r\n",
                        "name": "30.txt"
                    },
                    {
                        "input": "576460752313514584\n864691128465226328\n",
                        "output": "576460752293332392\r\n",
                        "name": "31.txt"
                    },
                    {
                        "input": "809253743786126225\n809253743786650513\n",
                        "output": "595055\r\n",
                        "name": "32.txt"
                    },
                    {
                        "input": "18014398509482004\n20266198323167252\n",
                        "output": "4503599627370476\r\n",
                        "name": "33.txt"
                    },
                    {
                        "input": "448121392887063642\n448121392887063898\n",
                        "output": "422\r\n",
                        "name": "34.txt"
                    },
                    {
                        "input": "217570419500574453\n217570423795540725\n",
                        "output": "5100869899\r\n",
                        "name": "35.txt"
                    },
                    {
                        "input": "477725013314697090\n477725013314697153\n",
                        "output": "126\r\n",
                        "name": "36.txt"
                    },
                    {
                        "input": "70277646023185\n70278115785233\n",
                        "output": "868158430\r\n",
                        "name": "37.txt"
                    },
                    {
                        "input": "951283588958958905\n951283588960531769\n",
                        "output": "2790798\r\n",
                        "name": "38.txt"
                    },
                    {
                        "input": "576460752303423489\n864691128455135233\n",
                        "output": "576460752303423487\r\n",
                        "name": "39.txt"
                    },
                    {
                        "input": "40005455732277247\n40005490083134111\n",
                        "output": "68685922305\r\n",
                        "name": "40.txt"
                    },
                    {
                        "input": "702631914103037613\n711611550434203925\n",
                        "output": "17944022787179174\r\n",
                        "name": "41.txt"
                    },
                    {
                        "input": "122661618998345727\n122661618998472719\n",
                        "output": "229377\r\n",
                        "name": "42.txt"
                    },
                    {
                        "input": "292733975779090434\n294985775592771584\n",
                        "output": "4503599627362300\r\n",
                        "name": "43.txt"
                    },
                    {
                        "input": "469500299002175157\n469535466194394801\n",
                        "output": "70327406314134\r\n",
                        "name": "44.txt"
                    },
                    {
                        "input": "867476329384116225\n867476346295549952\n",
                        "output": "33822867454\r\n",
                        "name": "45.txt"
                    },
                    {
                        "input": "33554434\n72057594054705152\n",
                        "output": "144115188042301436\r\n",
                        "name": "46.txt"
                    },
                    {
                        "input": "447835716237844145\n447835716773666481\n",
                        "output": "803807567\r\n",
                        "name": "47.txt"
                    },
                    {
                        "input": "953347253387133444\n953347253387133698\n",
                        "output": "508\r\n",
                        "name": "48.txt"
                    },
                    {
                        "input": "200269523239305216\n200269527534141440\n",
                        "output": "8589672448\r\n",
                        "name": "49.txt"
                    },
                    {
                        "input": "601265199245354673\n601265199245419185\n",
                        "output": "72015\r\n",
                        "name": "50.txt"
                    },
                    {
                        "input": "1\n1\n",
                        "output": "1\r\n",
                        "name": "51.txt"
                    },
                    {
                        "input": "1\n3\n",
                        "output": "3\r\n",
                        "name": "52.txt"
                    },
                    {
                        "input": "7\n8\n",
                        "output": "3\r\n",
                        "name": "53.txt"
                    },
                    {
                        "input": "10\n18\n",
                        "output": "16\r\n",
                        "name": "54.txt"
                    },
                    {
                        "input": "126\n252\n",
                        "output": "130\r\n",
                        "name": "55.txt"
                    },
                    {
                        "input": "200\n300\n",
                        "output": "176\r\n",
                        "name": "56.txt"
                    },
                    {
                        "input": "7\n9\n",
                        "output": "4\r\n",
                        "name": "s1.txt"
                    },
                    {
                        "input": "65\n98\n",
                        "output": "63\r\n",
                        "name": "s2.txt"
                    },
                    {
                        "input": "271828182845904523\n314159265358979323\n",
                        "output": "68833183630578410\r\n",
                        "name": "s3.txt"
                    },
                ],
                "name": "A or...or B Problem",
                "context": {
                    "contest": {
                        "name": "AtCoder Grand Contest 015",
                        "url": "https://atcoder.jp/contests/agc015",
                    },
                    "alphabet": "D",
                },
                "memoryLimit": 256,
                "timeLimit": 2000,
            },
        }
        actual = main(['get-problem', '--system', url], debug=True)
        self.assertEqual(expected, actual)
