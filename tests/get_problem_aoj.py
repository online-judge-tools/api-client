import hashlib
import unittest

from onlinejudge_api.main import main


class GetProblemAOJTest(unittest.TestCase):
    def test_1371(self):
        url = 'http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=1371'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=1371",
                "tests": [{
                    "input": "ACM\n",
                    "output": "0\n"
                }, {
                    "input": "icpc\n",
                    "output": "1\n"
                }, {
                    "input": "BAYL0R\n",
                    "output": "3\n"
                }, {
                    "input": "-AB+AC-A\n",
                    "output": "1\n"
                }, {
                    "input": "abcdefghi\n",
                    "output": "0\n"
                }, {
                    "input": "111-10=1+10*10\n",
                    "output": "1\n"
                }, {
                    "input": "0=10-1\n",
                    "output": "0\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_2310(self):
        url = 'http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=2310&lang=jp'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=2310",
                "tests": [{
                    "input": "3 5\n##..#\n#..##\n####.\n",
                    "output": "4\n"
                }, {
                    "input": "3 3\n#.#\n###\n#.#\n",
                    "output": "3\n"
                }, {
                    "input": "10 9\n.........\n.........\n####.....\n#..#.##..\n#..#..#..\n#..##.###\n#..##...#\n##..##.##\n###.#..#.\n###.####.\n",
                    "output": "6\n"
                }, {
                    "input": "10 11\n###########\n#.#.#.#.#.#\n#.#.#.#.#.#\n#.#.#.#.#.#\n#.#.#.#.#.#\n#.#.#.#.#.#\n#.#.#.#.#.#\n#.#.#.#.#.#\n#.#.#.#.#.#\n#.#.#.#.#.#\n",
                    "output": "7\n"
                }, {
                    "input": "25 38\n...........#...............#..........\n...........###..........####..........\n...........#####.......####...........\n............###############...........\n............###############...........\n............##############............\n.............#############............\n............###############...........\n...........#################..........\n.......#...#################...#......\n.......##.##################..##......\n........####################.##.......\n..........####################........\n.........#####..########..#####.......\n.......######....#####....######......\n......########...#####..########.#....\n....#######..#...#####..#..########...\n..#########.....#######......#######..\n...#######......#######........###....\n..####.........#########........###...\n...............#########..............\n..............##########..............\n..............##########..............\n...............########...............\n...............########...............\n",
                    "output": "8\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_2511(self):
        url = 'http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=2511'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=2511",
                "tests": [{
                    "input": "3 3\n1\n2\n3\n1 2 1\n1 3 1\n2 3 10\n3 2\n100\n10000\n1000000\n1 2 2\n1 3 3\n6 6\n2\n3\n5\n7\n11\n13\n1 3 17\n3 5 19\n5 1 23\n2 4 29\n4 6 31\n6 2 37\n11 16\n74\n25\n3\n39\n55\n18\n74\n55\n74\n3\n18\n1 7 200\n9 1 423\n2 9 205\n6 2 255\n2 5 123\n4 2 193\n2 3 200\n10 2 333\n2 11 256\n3 10 171\n4 10 512\n1 2 201\n8 5 314\n6 7 150\n11 6 257\n7 9 315\n20 38\n412516\n185397\n509168\n712745\n966959\n101213\n666120\n790528\n275431\n677098\n623178\n240167\n4371\n299088\n925699\n72800\n121416\n796859\n810604\n142754\n13 5 1000000\n3 7 991832\n10 1 781938\n15 8 455731\n1 3 655887\n1 20 604802\n19 10 452912\n15 5 360121\n10 15 256967\n9 5 682599\n8 7 917302\n5 18 974821\n2 19 790778\n17 5 298105\n15 11 132405\n18 19 745543\n2 4 790778\n1 2 790778\n11 14 269668\n15 4 882901\n1 14 522591\n15 18 424799\n9 19 712540\n20 5 592132\n18 17 770826\n19 8 592380\n16 5 258739\n8 4 794157\n3 18 569611\n7 19 340021\n19 11 803293\n8 18 692318\n9 6 626882\n20 2 592133\n2 17 196463\n12 14 506077\n16 20 928375\n12 18 894053\n0 0\n",
                    "output": "11\n5\n0\n2013\n9658580\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)


class GetProblemAOJSystemTest(unittest.TestCase):
    def test_itp1_1_b(self):
        url = 'http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B",
                "tests": [{
                    "input": "1\n",
                    "output": "1\n",
                    "name": "test1"
                }, {
                    "input": "3\n",
                    "output": "27\n",
                    "name": "test2"
                }, {
                    "input": "64\n",
                    "output": "262144\n",
                    "name": "test3"
                }, {
                    "input": "100\n",
                    "output": "1000000\n",
                    "name": "test4"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', '--system', url], debug=True)
        self.assertEqual(expected, actual)

    def test_1169(self):
        url = 'http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=1169&lang=jp'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=1169",
                "tests": [{
                    "input": 'f0ecaede832a038d0e940c2c4d0ab5e5',
                    "output": '8d2f7846dc2fc10ef37dcb548635c788',
                    "name": "judge_data"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', '--system', url], debug=True)
        for test in actual['result']['tests']:
            test['input'] = hashlib.md5(test['input'].encode()).hexdigest()
            test['output'] = hashlib.md5(test['output'].encode()).hexdigest()
        self.assertEqual(expected, actual)


class GetProblemAOJArenaTest(unittest.TestCase):
    def test_yupro_d(self):
        url = 'https://onlinejudge.u-aizu.ac.jp/services/room.html#yupro/problems/D'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://onlinejudge.u-aizu.ac.jp/services/room.html#yupro/problems/D",
                "tests": [{
                    "input": "6/2*(1+2)\n1-1-1\n(1-1-1)/2\n#\n",
                    "output": "2\n2\n1\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)
