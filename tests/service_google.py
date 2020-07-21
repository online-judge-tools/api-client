import textwrap
import unittest

from onlinejudge.service.google import GoogleCodeJamProblem, GoogleCodeJamService
from onlinejudge.type import TestCase


class GoogleCodeJamSerivceTest(unittest.TestCase):
    def test_from_url(self):
        self.assertIsInstance(GoogleCodeJamService.from_url('https://codingcompetitions.withgoogle.com/'), GoogleCodeJamService)
        self.assertIsInstance(GoogleCodeJamService.from_url('https://code.google.com/codejam'), GoogleCodeJamService)
        self.assertIsNone(GoogleCodeJamService.from_url('https://code.google.com/'))
        self.assertIsNone(GoogleCodeJamService.from_url('https://www.facebook.com/hackercup'))


class GoogleCodeJamProblemTest(unittest.TestCase):
    def test_from_url_codejam(self):
        problem = GoogleCodeJamProblem.from_url('https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/000000000020993c')
        self.assertEqual(problem.domain, 'codingcompetitions.withgoogle.com')
        self.assertEqual(problem.kind, 'codejam')
        self.assertEqual(problem.contest_id, '000000000019fd27')
        self.assertEqual(problem.problem_id, '000000000020993c')

    def test_from_url_kickstart(self):
        problem = GoogleCodeJamProblem.from_url('https://codingcompetitions.withgoogle.com/kickstart/round/000000000019ffc7/00000000001d3f56')
        self.assertEqual(problem.domain, 'codingcompetitions.withgoogle.com')
        self.assertEqual(problem.kind, 'kickstart')
        self.assertEqual(problem.contest_id, '000000000019ffc7')
        self.assertEqual(problem.problem_id, '00000000001d3f56')

    def test_from_url_old(self):
        problem = GoogleCodeJamProblem.from_url('https://code.google.com/codejam/contest/7234486/dashboard#s=p2')
        self.assertEqual(problem.domain, 'code.google.com')
        self.assertEqual(problem.kind, 'codejam')
        self.assertEqual(problem.contest_id, '7234486')
        self.assertEqual(problem.problem_id, 'p2')

    def test_from_url_old_no_fragment(self):
        problem = GoogleCodeJamProblem.from_url('https://code.google.com/codejam/contest/8404486/dashboard')
        self.assertEqual(problem.domain, 'code.google.com')
        self.assertEqual(problem.kind, 'codejam')
        self.assertEqual(problem.contest_id, '8404486')
        self.assertEqual(problem.problem_id, 'p0')

    def test_download_samples_codejam(self):
        problem = GoogleCodeJamProblem.from_url('https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/000000000020993c')
        sample_input = textwrap.dedent("""\
            3
            4
            1 2 3 4
            2 1 4 3
            3 4 1 2
            4 3 2 1
            4
            2 2 2 2
            2 3 2 3
            2 2 2 3
            2 2 2 2
            3
            2 1 3
            1 3 2
            1 2 3
            """).encode()
        sample_output = textwrap.dedent("""\
            Case #1: 4 0 0
            Case #2: 9 4 4
            Case #3: 8 0 2
            """).encode()
        self.assertEqual(problem.download_sample_cases(), [
            TestCase(
                'sample-1',
                'Input 1',
                sample_input,
                'Output 1',
                sample_output,
            ),
        ])

    def test_download_samples_kickstart(self):
        problem = GoogleCodeJamProblem.from_url('https://codingcompetitions.withgoogle.com/kickstart/round/000000000019ffc7/00000000001d3f56')
        sample_input = textwrap.dedent("""\
            3
            4 100
            20 90 40 90
            4 50
            30 30 10 10
            3 300
            999 999 999
            """).encode()
        sample_output = textwrap.dedent("""\
            Case #1: 2
            Case #2: 3
            Case #3: 0
            """).encode()
        self.assertEqual(problem.download_sample_cases(), [
            TestCase(
                'sample-1',
                'Input 1',
                sample_input,
                'Output 1',
                sample_output,
            ),
        ])

    def test_download_multiple_samples(self):
        problem = GoogleCodeJamProblem.from_url('https://codingcompetitions.withgoogle.com/kickstart/round/000000000019ffc7/00000000001d3ff3')
        sample_input1 = textwrap.dedent("""\
            2
            2 2
            KICK
            START
            8 2
            G
            G
            GO
            GO
            GOO
            GOO
            GOOO
            GOOO
            """).encode()
        sample_output1 = textwrap.dedent("""\
            Case #1: 0
            Case #2: 10
            """).encode()
        sample_input2 = textwrap.dedent("""\
            1
            6 3
            RAINBOW
            FIREBALL
            RANK
            RANDOM
            FIREWALL
            FIREFIGHTER
            """).encode()
        sample_output2 = textwrap.dedent("""\
            Case #1: 6
            """).encode()
        self.assertEqual(problem.download_sample_cases(), [
            TestCase(
                'sample-1',
                'Input 1',
                sample_input1,
                'Output 1',
                sample_output1,
            ),
            TestCase(
                'sample-2',
                'Input 2',
                sample_input2,
                'Output 2',
                sample_output2,
            ),
        ])

    @unittest.expectedFailure  # GCJ is now porting old problems to the new platform
    def test_download_samples_old(self):
        problem = GoogleCodeJamProblem.from_url('https://code.google.com/codejam/contest/7234486/dashboard#s=p2')
        sample_input = textwrap.dedent("""\
            4
            4 100000
            4 300000
            3 300000
            100 499999
            """).encode()
        sample_output = textwrap.dedent("""\
            Case #1: 9
            Case #2: 7
            Case #3: 5
            Case #4: 3
            """).encode()
        self.assertEqual(problem.download_sample_cases(), [
            TestCase(
                'sample-1',
                'Input 1',
                sample_input,
                'Output 1',
                sample_output,
            ),
        ])
