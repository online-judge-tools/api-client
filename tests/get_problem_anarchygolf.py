import unittest

from onlinejudge_api.main import main


class GetProblemAnarchyGolfTest(unittest.TestCase):
    def test_hello_world(self):
        url = 'http://golf.shinh.org/p.rb?hello+world'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://golf.shinh.org/p.rb?hello+world",
                "tests": [
                    {
                        "input": "",
                        "output": "Hello, world!\n"
                    },
                ],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_simple_language(self):
        url = 'http://golf.shinh.org/p.rb?simple+language'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://golf.shinh.org/p.rb?simple+language",
                "tests": [
                    {
                        "input": "2+2",
                        "output": "4"
                    },
                    {
                        "input": "a:{x.2+x}\na2",
                        "output": "4"
                    },
                    {
                        "input": "ack:{m n.if (m=0){n+1}{if (n=0){ack (m-1) 1}{ack (m-1) (ack m (n-1))}}}\nfact:{n.if (n=0){1}{n*(fact (n-1))}}\nack 3 4\nfact 4",
                        "output": "125\n24"
                    },
                ],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)

    def test_momomo(self):
        """test_momomo() tests a problem whose test case contains Japanese letters.
        """

        url = 'http://golf.shinh.org/p.rb?momomo'
        expected = {
            "status": "ok",
            "messages": [],
            "result": {
                "url": "http://golf.shinh.org/p.rb?momomo",
                "tests": [
                    {
                        "input": "も\nもも\nももも\nもももも\nももももも\nもももももも\nももももももも\nもももももももも\nももももももももも\nもももももももももも\nももももももももももも\nもももももももももももも\nももももももももももももも\nもももももももももももももも\nももももももももももももももも\nもももももももももももももももも\nももももももももももももももももも\nもももももももももももももももももも\nももももももももももももももももももも\nもももももももももももももももももももも\nももももももももももももももももももももも\nもももももももももももももももももももももも\nももももももももももももももももももももももも\nもももももももももももももももももももももももも\nももももももももももももももももももももももももも\nもももももももももももももももももももももももももも\nももももももももももももももももももももももももももも\nもももももももももももももももももももももももももももも\nももももももももももももももももももももももももももももも\nもももももももももももももももももももももももももももももも\n",
                        "output": "Also\nPeaches\nMomomo\nMomomo\nMomomo thighs\nMomomo thighs as well\nMomomomomomomo\nMomomo thighs peach\nMomo, thigh, moat\nMomomo thighs, peaches, and thighs\nMomomo thighs thighs thighs\nMomomo thighs, peaches, thighs\nMomomo peach thigh, thigh, thigh, as well\nMombers and thighs, peels, thighs, peaches\nMomo thombomomed thigh, thigh, thigh, thigh, as well\nThe thighs, the thighs, the thighs, the thighs, the thighs, the thighs and the thighs\nMomomo thighs as well as thighs, bamboo thigh, thigh, thigh, as well\nThe thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thighs\nMomomo thighs as well as thighs, bamboo thigh, thigh, thigh, thigh, as well\nThe thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs and the thighs\nMomomo thighs as well as thighs, peeling, thighs, thighs, thighs, thighs, thighs, thighs\nThe thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs and the thighs\nMomomo thighs as well as thighs, thighs, thighs, thighs, thighs, thighs, thighs, thigh, and thigh\nBesides the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs and the thighs\nMomo thighs as well as thighs, thighs, thighs, thighs, thighs, thighs, thighs, thighs, pebbles, thigh\nThe thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thigh\nThe thighs as well as the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs,\nThe thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh,\nThe thighs and the thighs as well as the thighs, the thighs, the thighs, the thighs, the thighs, the thighs, the thighs,\nThe thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh, the thigh each\n"
                    },
                ],
                "context": {}
            },
        }
        actual = main(['get-problem', url], debug=True)
        self.assertEqual(expected, actual)
