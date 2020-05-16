import unittest

from onlinejudge.service.topcoder import TopcoderProblem, TopcoderService


class TopcoderSerivceTest(unittest.TestCase):
    def test_from_url(self):
        self.assertIsInstance(TopcoderService.from_url('https://topcoder.com/'), TopcoderService)
        self.assertIsInstance(TopcoderService.from_url('https://arena.topcoder.com/'), TopcoderService)
        self.assertIsInstance(TopcoderService.from_url('https://community.topcoder.com/'), TopcoderService)
        self.assertIsNone(TopcoderService.from_url('https://atcoder.jp/'))


class TopcoderProblemTest(unittest.TestCase):
    def test_from_url(self):
        self.assertEqual(TopcoderProblem.from_url('https://arena.topcoder.com/index.html#/u/practiceCode/14230/10838/10760/1/303803').problem_id, 10760)
        self.assertEqual(TopcoderProblem.from_url('https://community.topcoder.com/stat?c=problem_statement&pm=10760').problem_id, 10760)
        self.assertIsNone(TopcoderProblem.from_url('https://atcoder.jp/contests/abc141/tasks/abc141_b'))
