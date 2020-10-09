import os
import unittest

from onlinejudge_api.main import main

YUKICODER_TOKEN = os.environ.get('YUKICODER_TOKEN')


class GetProblemYukicoderTest(unittest.TestCase):
    def test_100(self):
        """This tests about sample cases.
        """

        url = 'http://yukicoder.me/problems/100'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "https://yukicoder.me/problems/100",
                "tests": [{
                    "input": "30\n5\n",
                    "output": "19\n"
                }, {
                    "input": "100\n2\n",
                    "output": "75\n"
                }, {
                    "input": "100000\n1\n",
                    "output": "100000\n"
                }],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    @unittest.skipIf(YUKICODER_TOKEN is None, '$YUKICODER_TOKEN is required')
    def test_2_system(self):
        """This tests about system cases.
        """

        url = 'https://yukicoder.me/problems/no/2'
        expected = {"status": "ok", "messages": [], "result": {"url": "https://yukicoder.me/problems/no/2", "tests": [{"input": "4\n", "output": "Alice\n", "name": "01.txt"}, {"input": "11\n", "output": "Alice\n", "name": "02.txt"}, {"input": "24\n", "output": "Alice\n", "name": "03.txt"}, {"input": "600\n", "output": "Bob\n", "name": "04.txt"}, {"input": "1191\n", "output": "Bob\n", "name": "05.txt"}, {"input": "111111\n", "output": "Alice\n", "name": "06.txt"}, {"input": "12344321\n", "output": "Bob\n", "name": "07.txt"}, {"input": "14153200\n", "output": "Alice\n", "name": "08.txt"}, {"input": "12865745\n", "output": "Bob\n", "name": "09.txt"}, {"input": "100000000\n", "output": "Bob\n", "name": "10.txt"}, {"input": "85050396\n", "output": "Bob\n", "name": "99_system_test1.txt"}, {"input": "39942450\n", "output": "Alice\n", "name": "99_system_test2.txt"}, {"input": "39871926\n", "output": "Alice\n", "name": "99_system_test3.txt"}, {"input": "81107712\n", "output": "Alice\n", "name": "99_system_test4.txt"}, {"input": "7300208\n", "output": "Alice\n", "name": "challenge01.txt"}, {"input": "23426659\n", "output": "Bob\n", "name": "challenge02.txt"}, {"input": "58041938\n", "output": "Alice\n", "name": "challenge03.txt"}, {"input": "86955032\n", "output": "Alice\n", "name": "challenge04.txt"}, {"input": "93598141\n", "output": "Alice\n", "name": "challenge05.txt"}, {"input": "53670893\n", "output": "Alice\n", "name": "challenge06.txt"}, {"input": "71653262\n", "output": "Bob\n", "name": "challenge07.txt"}, {"input": "97117687\n", "output": "Alice\n", "name": "challenge08.txt"}, {"input": "89261532\n", "output": "Alice\n", "name": "challenge09.txt"}, {"input": "41516943\n", "output": "Bob\n", "name": "system_test1.txt"}, {"input": "93764929\n", "output": "Bob\n", "name": "system_test2.txt"}, {"input": "69426035\n", "output": "Alice\n", "name": "system_test3.txt"}, {"input": "48741327\n", "output": "Alice\n", "name": "system_test4.txt"}, {"input": "25670140\n", "output": "Alice\n", "name": "system_test5.txt"}, {"input": "55650694\n", "output": "Alice\n", "name": "system_test6.txt"}, {"input": "45411477\n", "output": "Alice\n", "name": "system_test7.txt"}, {"input": "42323399\n", "output": "Bob\n", "name": "system_test8.txt"}], "context": {}}}
        actual = main(['get-problem', '--system', url], debug=True)
        self.assertEqual(expected, actual)
