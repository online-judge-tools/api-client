import unittest

from onlinejudge.service.codechef import CodeChefProblem, CodeChefService
from onlinejudge.type import TestCase


class CodeChefSerivceTest(unittest.TestCase):
    def test_from_url(self):
        self.assertIsInstance(CodeChefService.from_url('https://www.codechef.com/'), CodeChefService)
        self.assertIsNone(CodeChefService.from_url('https://www.facebook.com/'))


class CodeChefProblemTest(unittest.TestCase):
    def test_from_url(self):
        self.assertEqual(CodeChefProblem.from_url('https://www.codechef.com/COOK113A/problems/DAND').contest_id, 'COOK113A')
        self.assertEqual(CodeChefProblem.from_url('https://www.codechef.com/COOK113A/problems/DAND').problem_id, 'DAND')

    def test_download_samples_chfgcd(self):
        url = 'https://www.codechef.com/COOK131B/problems/CHFGCD'
        expected = [
            TestCase(name='sample-1', input_name='input', input_data=b'2\n4 16\n4 55\n', output_name='output', output_data=b'0\n1\n'),
        ]
        self.assertEqual(CodeChefProblem.from_url(url).download_sample_cases(), expected)

    # TODO: support problems with an old format
    @unittest.expectedFailure
    def test_download_samples_dand(self):
        url = 'https://www.codechef.com/COOK113A/problems/DAND'
        expected = [
            TestCase(name='sample-1', input_name='input', input_data=b'6\n1 9 3\n4 7 1\n10 75 12\n3 8 3\n5 10 2\n192 913893 3812\n', output_name='output', output_data=b'4\n7\n64\n4\n8\n909312\n'),
        ]
        self.assertEqual(CodeChefProblem.from_url(url).download_sample_cases(), expected)

    # TODO: support problems with an old format
    @unittest.expectedFailure
    def test_download_samples_cntset(self):
        url = 'https://www.codechef.com/PLIN2020/problems/CNTSET'
        expected = [
            TestCase(name='sample-1', input_name='input', input_data=b'4 2\n', output_name='output', output_data=b'12\n'),
        ]
        self.assertEqual(CodeChefProblem.from_url(url).download_sample_cases(), expected)

    # TODO: support problems with an old format
    @unittest.expectedFailure
    def test_download_samples_acesqn(self):
        url = 'https://www.codechef.com/CNES2017/problems/ACESQN'
        expected = [
            TestCase(name='sample-1', input_name='input', input_data=b'1\n5\n1 2 3 4 5\n', output_name='output', output_data=b'2\n'),
        ]
        self.assertEqual(CodeChefProblem.from_url(url).download_sample_cases(), expected)
