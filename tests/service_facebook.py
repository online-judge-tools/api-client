import unittest

from onlinejudge.service.facebook import FacebookHackerCupProblem, FacebookHackerCupService
from onlinejudge.type import TestCase


class FacebookHackerCupSerivceTest(unittest.TestCase):
    def test_from_url(self):
        self.assertIsInstance(FacebookHackerCupService.from_url('https://www.facebook.com/hackercup/'), FacebookHackerCupService)
        self.assertIsInstance(FacebookHackerCupService.from_url('https://www.facebook.com/hackercup/problem/448364075989193/'), FacebookHackerCupService)
        self.assertIsInstance(FacebookHackerCupService.from_url('https://www.facebook.com/codingcompetitions/'), FacebookHackerCupService)
        self.assertIsNone(FacebookHackerCupService.from_url('https://www.facebook.com/AtCoder/'))


class FacebookHackerCupProblemTest(unittest.TestCase):
    def test_from_url(self):
        self.assertIsNone(FacebookHackerCupProblem.from_url('https://www.facebook.com/hackercup/problem/448364075989193/'))
        self.assertEqual(FacebookHackerCupProblem.from_url('https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/D1').series_vanity, 'hacker-cup')
        self.assertEqual(FacebookHackerCupProblem.from_url('https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/D1').season_vanity, '2020')
        self.assertEqual(FacebookHackerCupProblem.from_url('https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/D1').contest_vanity, 'qualification-round')
        self.assertEqual(FacebookHackerCupProblem.from_url('https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/D1').display_index, 'D1')
