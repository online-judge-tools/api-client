# -*- coding: utf-8 -*-
import unittest

import requests

from onlinejudge.service.atcoder import AtCoderContest, AtCoderProblem, AtCoderProblemDetailedData, AtCoderService, AtCoderSubmission
from onlinejudge.type import TestCase


class AtCoderSerivceTest(unittest.TestCase):
    def test_from_url(self):
        self.assertIsInstance(AtCoderService.from_url('https://atcoder.jp/'), AtCoderService)
        self.assertIsInstance(AtCoderService.from_url('https://beta.atcoder.jp/'), AtCoderService)
        self.assertIsInstance(AtCoderService.from_url('https://abc001.contest.atcoder.jp/'), AtCoderService)
        self.assertIsInstance(AtCoderService.from_url('https://atcoder.jp/contests/agc001/submissions/806160'), AtCoderService)
        self.assertIsNone(AtCoderService.from_url('https://codeforces.com/'))

    def test_iterate_contests(self):
        contests = list(AtCoderService().iterate_contests())
        contest_ids = [contest.contest_id for contest in contests]
        self.assertIn('arc001', contest_ids)
        self.assertIn('abc100', contest_ids)
        self.assertIn('kupc2012', contest_ids)
        contest, = [contest for contest in contests if contest.contest_id == 'utpc2013']
        data = contest.download_data()
        self.assertEqual(data.start_time.year, 2014)
        self.assertEqual(data.start_time.month, 3)
        self.assertEqual(data.start_time.day, 2)
        self.assertEqual(data.name, '東京大学プログラミングコンテスト2013')
        self.assertEqual(data.duration.total_seconds(), 5 * 60 * 60)
        self.assertEqual(data.rated_range, '-')


class AtCoderContestTest(unittest.TestCase):
    def test_from_url(self):
        self.assertEqual(AtCoderContest.from_url('https://kupc2014.contest.atcoder.jp/tasks/kupc2014_d').contest_id, 'kupc2014')
        self.assertEqual(AtCoderContest.from_url('https://atcoder.jp/contests/agc030').contest_id, 'agc030')
        self.assertIsNone(AtCoderContest.from_url('https://atcoder.jp/contests/'))

    def test_load_details(self):
        contest = AtCoderContest.from_url('https://atcoder.jp/contests/keyence2019')
        self.assertEqual(contest.download_data(lang='en').name, 'KEYENCE Programming Contest 2019')
        self.assertEqual(contest.download_data(lang='ja').name, 'キーエンス プログラミング コンテスト 2019')
        data = contest.download_data()
        self.assertEqual(data.start_time.year, 2019)
        self.assertEqual(data.start_time.month, 1)
        self.assertEqual(data.start_time.day, 13)
        self.assertEqual(data.duration.total_seconds(), 2 * 60 * 60)
        self.assertEqual(data.can_participate, 'All')
        self.assertEqual(data.rated_range, ' - 2799')
        self.assertEqual(data.penalty.total_seconds(), 5 * 60)

        contest = AtCoderContest.from_url('https://atcoder.jp/contests/dp')
        self.assertEqual(contest.download_data(lang='ja').name, 'Educational DP Contest / DP まとめコンテスト')
        self.assertEqual(contest.download_data(lang='en').name, 'Educational DP Contest')
        data = contest.download_data()
        self.assertEqual(data.start_time.year, 2019)
        self.assertEqual(data.start_time.month, 1)
        self.assertEqual(data.start_time.day, 6)
        self.assertEqual(data.duration.total_seconds(), 5 * 60 * 60)
        self.assertEqual(data.can_participate, 'All')
        self.assertEqual(data.rated_range, '-')
        self.assertEqual(data.penalty.total_seconds(), 5 * 60)

    def test_get_penalty_a_singular_form(self):
        contest = AtCoderContest.from_url('https://atcoder.jp/contests/chokudai_S002')
        self.assertEqual(contest.download_data().penalty.total_seconds(), 60)  # Penalty is written as "1 minute", not  "1 minutes"

    def test_list_problems(self):
        contest = AtCoderContest.from_url('https://atcoder.jp/contests/agc028')
        problems = contest.list_problems()
        self.assertEqual(len(problems), 7)
        self.assertEqual(problems[0].download_data().alphabet, 'A')
        self.assertEqual(problems[0].download_data().name, 'Two Abbreviations')
        self.assertEqual(problems[0].download_data().time_limit_msec, 2000)
        self.assertEqual(problems[0].download_data().memory_limit_byte, 1024 * 1000 * 1000)
        self.assertEqual(problems[5].download_data().alphabet, 'F')
        self.assertEqual(problems[5].problem_id, 'agc028_f')
        self.assertEqual(problems[6].download_data().alphabet, 'F2')
        self.assertEqual(problems[6].problem_id, 'agc028_f2')

    def test_list_problems_with_float_values(self):
        """
        .. seealso:
            https://github.com/kmyk/online-judge-tools/issues/412
        """

        contest = AtCoderContest.from_url('https://atcoder.jp/contests/dwacon2018-final-open')
        problems = contest.list_problems()
        self.assertEqual(problems[0].download_data().time_limit_msec, 2525)
        self.assertEqual(problems[0].download_data().memory_limit_byte, 246 * 1000 * 1000)
        self.assertEqual(problems[1].download_data().time_limit_msec, 5252)
        self.assertEqual(problems[1].download_data().memory_limit_byte, 512 * 1000 * 1000)

    def test_list_problems_time_limit_is_less_than_msec(self):
        contest = AtCoderContest.from_url('https://atcoder.jp/contests/joi2019ho')
        problems = contest.list_problems()
        self.assertEqual(problems[0].download_data().time_limit_msec, 1000)
        self.assertEqual(problems[1].download_data().time_limit_msec, 1000)
        self.assertEqual(problems[2].download_data().time_limit_msec, 500)
        self.assertEqual(problems[3].download_data().time_limit_msec, 1000)
        self.assertEqual(problems[4].download_data().time_limit_msec, 2000)

    def test_list_problems_memory_limit_is_zero(self):
        contest = AtCoderContest.from_url('https://atcoder.jp/contests/future-contest-2019-final-open')
        problems = contest.list_problems()
        self.assertEqual(problems[0].download_data().memory_limit_byte, 1024 * 1000 * 1000)  # 1024 MB
        self.assertEqual(problems[1].download_data().memory_limit_byte, 0)  # 0 KB

    def test_iterate_submissions(self):
        contest = AtCoderContest.from_url('https://atcoder.jp/contests/code-festival-2014-exhibition-open')
        submissions = list(contest.iterate_submissions())
        self.assertGreater(len(submissions), 300)
        self.assertEqual(submissions[0].get_url(), 'https://atcoder.jp/contests/code-festival-2014-exhibition-open/submissions/272697')
        self.assertEqual(submissions[1].get_url(), 'https://atcoder.jp/contests/code-festival-2014-exhibition-open/submissions/272700')

    def test_get_contest_without_penalty(self):
        contest = AtCoderContest.from_url('https://atcoder.jp/contests/otemae2019')
        self.assertEqual(contest.download_data(lang='ja').name, '大手前プロコン 2019')
        self.assertEqual(contest.download_data().penalty.total_seconds(), 0)  # This contest has no penalty
        self.assertEqual(contest.download_data(lang='en').name, 'Otemae High School Programming Contest 2019')
        self.assertEqual(contest.download_data().penalty.total_seconds(), 0)  # This contest has no penalty


class AtCoderProblemTest(unittest.TestCase):
    def test_from_url(self):
        self.assertEqual(AtCoderProblem.from_url('https://kupc2014.contest.atcoder.jp/tasks/kupc2014_d').contest_id, 'kupc2014')
        self.assertEqual(AtCoderProblem.from_url('https://kupc2014.contest.atcoder.jp/tasks/kupc2014_d').problem_id, 'kupc2014_d')
        self.assertEqual(AtCoderProblem.from_url('http://jag2013spring.contest.atcoder.jp/tasks/icpc2013spring_a').contest_id, 'jag2013spring')
        self.assertEqual(AtCoderProblem.from_url('http://jag2013spring.contest.atcoder.jp/tasks/icpc2013spring_a').problem_id, 'icpc2013spring_a')
        self.assertEqual(AtCoderProblem.from_url('https://beta.atcoder.jp/contests/abc073/tasks/abc073_a').contest_id, 'abc073')
        self.assertEqual(AtCoderProblem.from_url('https://beta.atcoder.jp/contests/abc073/tasks/abc073_a').problem_id, 'abc073_a')
        self.assertEqual(AtCoderProblem.from_url('https://beta.atcoder.jp/contests/ddcc2017-qual/tasks/ddcc2017_qual_a').contest_id, 'ddcc2017-qual')
        self.assertEqual(AtCoderProblem.from_url('https://beta.atcoder.jp/contests/ddcc2017-qual/tasks/ddcc2017_qual_a').problem_id, 'ddcc2017_qual_a')
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/agc030/tasks/agc030_c').contest_id, 'agc030')
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/agc030/tasks/agc030_c').problem_id, 'agc030_c')

    def test_from_url_with_superfluous_things(self):
        """This tests unusual URLs.

        AtCoder uses query parameters like `?lang=en`.
        A service (AtCoder Virtual Contest https://not-522.appspot.com/) sometimes makes URLs which contain `//` in their paths.
        """

        self.assertEqual(AtCoderProblem.from_url('http://agc001.contest.atcoder.jp//////tasks//////agc001_a//////?hoge=fuga#piyo').contest_id, 'agc001')
        self.assertEqual(AtCoderProblem.from_url('http://agc001.contest.atcoder.jp//////tasks//////agc001_a//////?hoge=fuga#piyo').problem_id, 'agc001_a')

    def test_repr(self):
        self.assertEqual(repr(AtCoderProblem(contest_id='kupc2014', problem_id='kupc2014_d')), "AtCoderProblem.from_url('https://atcoder.jp/contests/kupc2014/tasks/kupc2014_d')")
        self.assertEqual(repr(AtCoderProblem(contest_id='agc030', problem_id='agc030_c')), "AtCoderProblem.from_url('https://atcoder.jp/contests/agc030/tasks/agc030_c')")
        self.assertEqual(repr(AtCoderProblem(contest_id='xxxxxx', problem_id='yyyyyy')), "AtCoderProblem.from_url('https://atcoder.jp/contests/xxxxxx/tasks/yyyyyy')")

    def test_eq(self):
        self.assertEqual(AtCoderProblem.from_url('https://kupc2014.contest.atcoder.jp/tasks/kupc2014_d'), AtCoderProblem.from_url('https://atcoder.jp/contests/kupc2014/tasks/kupc2014_d'))
        self.assertNotEqual(AtCoderProblem.from_url('https://kupc2014.contest.atcoder.jp/tasks/kupc2014_d'), AtCoderProblem.from_url('https://atcoder.jp/contests/agc030/tasks/agc030_c'))

    def test_load_details(self):
        problem = AtCoderProblem.from_url('https://atcoder.jp/contests/abc118/tasks/abc118_a')
        data = problem.download_data()
        self.assertEqual(data.alphabet, 'A')
        self.assertEqual(data.name, 'B +/- A')
        self.assertEqual(data.time_limit_msec, 2000)
        self.assertEqual(data.memory_limit_byte, 1024 * 1000 * 1000)
        self.assertEqual(data.score, 100)

    def test_get_alphabet(self):
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/agc028/tasks/agc028_f').download_data().alphabet, 'F')
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/agc028/tasks/agc028_f2').download_data().alphabet, 'F2')

    def test_get_score(self):
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/future-contest-2018-final/tasks/future_contest_2018_final_a').download_data().score, 50000000)
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/abc001/tasks/abc001_4').download_data().score, None)

    def test_get_score_latex(self):
        """
        .. seealso::
            https://github.com/kmyk/online-judge-tools/issues/411
        """

        self.assertIsNone(AtCoderProblem.from_url('https://atcoder.jp/contests/wupc2019/tasks/wupc2019_a').download_data().score)

    def test_get_time_limit_is_less_than_msec(self):
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/joi2019ho/tasks/joi2019ho_c').download_data().time_limit_msec, 500)
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/future-contest-2019-qual/tasks/future_contest_2019_qual_b').download_data().time_limit_msec, 0)

    def test_get_memory_limit_is_zero(self):
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/future-contest-2019-qual/tasks/future_contest_2019_qual_b').download_data().memory_limit_byte, 0)

    def test_iterate_submissions(self):
        problem = AtCoderProblem.from_url('https://atcoder.jp/contests/abc119/tasks/abc119_c')
        submissions = problem.iterate_submissions()
        self.assertEqual(next(submissions).get_url(), 'https://atcoder.jp/contests/abc119/submissions/4368719')
        self.assertEqual(next(submissions).get_url(), 'https://atcoder.jp/contests/abc119/submissions/4368922')
        self.assertEqual(next(submissions).get_url(), 'https://atcoder.jp/contests/abc119/submissions/4369188')
        self.assertEqual(next(submissions).get_url(), 'https://atcoder.jp/contests/abc119/submissions/4369193')


class AtCoderSubmissionTest(unittest.TestCase):
    def test_from_url(self):
        self.assertEqual(AtCoderSubmission.from_url('https://atcoder.jp/contests/kupc2012/submissions/2097011').contest_id, 'kupc2012')
        self.assertEqual(AtCoderSubmission.from_url('https://atcoder.jp/contests/kupc2012/submissions/2097011').submission_id, 2097011)
        self.assertEqual(AtCoderSubmission.from_url('https://qupc2014.contest.atcoder.jp/submissions/1444440').contest_id, 'qupc2014')
        self.assertEqual(AtCoderSubmission.from_url('https://qupc2014.contest.atcoder.jp/submissions/1444440').submission_id, 1444440)


class AtCoderProblemDataTest(unittest.TestCase):
    def test_from_html_very_old(self):
        url = 'https://atcoder.jp/contests/utpc2011/tasks/utpc2011_1'
        resp = requests.get(url)
        html = resp.content.decode(resp.apparent_encoding)
        data = AtCoderProblemDetailedData.from_html(html, problem=AtCoderProblem.from_url(url))

        self.assertEqual(data.alphabet, 'A')
        self.assertEqual(data.available_languages, None)
        self.assertEqual(data.html, html)
        self.assertEqual(data.input_format, None)
        self.assertEqual(data.memory_limit_byte, 292 * 1000 * 1000)
        self.assertEqual(data.name, 'プログラミングコンテスト')
        self.assertEqual(data.problem, AtCoderProblem.from_url(url))
        self.assertEqual(data.sample_cases, [
            TestCase(name='sample-1', input_name='入力例 1:', input_data=b'3 4\n1 0 1 0\n1 1 1 0\n0 0 0 1\n', output_name='入力例 1 に対する出力例:', output_data=b'3\n'),
            TestCase(name='sample-2', input_name='入力例 2:', input_data=b'3 4\n1 1 1 1\n1 1 1 1\n1 1 1 1\n', output_name='入力例 2 に対する出力例:', output_data=b'4\n'),
            TestCase(name='sample-3', input_name='入力例 3:', input_data=b'1 1\n0\n', output_name='入力例 3 に対する出力例:', output_data=b'0\n'),
        ])
        self.assertEqual(data.score, None)
        self.assertEqual(data.time_limit_msec, 1 * 1000)

    def test_from_html_old(self):
        url = 'https://atcoder.jp/contests/abc003/tasks/abc003_4'
        resp = requests.get(url)
        html = resp.content.decode(resp.apparent_encoding)
        data = AtCoderProblemDetailedData.from_html(html, problem=AtCoderProblem.from_url(url))

        self.assertEqual(data.alphabet, 'D')
        self.assertEqual(data.available_languages, None)
        self.assertEqual(data.html, html)
        self.assertEqual(data.input_format, '\r\n<var>R</var> <var>C</var>\r\n<var>X</var> <var>Y</var>\r\n<var>D</var> <var>L</var>\r\n')
        self.assertEqual(data.memory_limit_byte, 64 * 1000 * 1000)
        self.assertEqual(data.name, 'AtCoder社の冬')
        self.assertEqual(data.problem, AtCoderProblem.from_url(url))
        self.assertEqual(data.sample_cases, [
            TestCase(name='sample-1', input_name='入力例 1', input_data=b'3 2\n2 2\n2 2\n', output_name='出力例 1', output_data=b'12\n'),
            TestCase(name='sample-2', input_name='入力例 2', input_data=b'4 5\n3 1\n3 0\n', output_name='出力例 2', output_data=b'10\n'),
            TestCase(name='sample-3', input_name='入力例 3', input_data=b'23 18\n15 13\n100 95\n', output_name='出力例 3', output_data=b'364527243\n'),
            TestCase(name='sample-4', input_name='入力例 4', input_data=b'30 30\n24 22\n145 132\n', output_name='出力例 4', output_data=b'976668549\n'),
        ])
        self.assertEqual(data.score, None)
        self.assertEqual(data.time_limit_msec, 2 * 1000)

    def test_from_html_standard(self):
        url = 'https://atcoder.jp/contests/abc114/tasks/abc114_d'
        resp = requests.get(url)
        html = resp.content.decode(resp.apparent_encoding)
        data = AtCoderProblemDetailedData.from_html(html, problem=AtCoderProblem.from_url(url))

        self.assertEqual(data.alphabet, 'D')
        self.assertEqual(data.available_languages, None)
        self.assertEqual(data.html, html)
        self.assertEqual(data.input_format, '<var>N</var>\r\n')
        self.assertEqual(data.memory_limit_byte, 1024 * 1000 * 1000)
        self.assertEqual(data.name, '756')
        self.assertEqual(data.problem, AtCoderProblem.from_url(url))
        self.assertEqual(data.sample_cases, [
            TestCase(name='sample-1', input_name='入力例 1', input_data=b'9\n', output_name='出力例 1', output_data=b'0\n'),
            TestCase(name='sample-2', input_name='入力例 2', input_data=b'10\n', output_name='出力例 2', output_data=b'1\n'),
            TestCase(name='sample-3', input_name='入力例 3', input_data=b'100\n', output_name='出力例 3', output_data=b'543\n'),
        ])
        self.assertEqual(data.score, 400)
        self.assertEqual(data.time_limit_msec, 2 * 1000)

    def test_from_html_with_empty_output(self):
        url = 'https://atcoder.jp/contests/agc036/tasks/agc036_b'
        resp = requests.get(url)
        html = resp.content.decode(resp.apparent_encoding)
        data = AtCoderProblemDetailedData.from_html(html, problem=AtCoderProblem.from_url(url))

        self.assertEqual(data.alphabet, 'B')
        self.assertEqual(data.available_languages, None)
        self.assertEqual(data.html, html)
        self.assertEqual(data.input_format, '<var>N</var> <var>K</var>\r\n<var>A_0</var> <var>A_1</var> <var>\\cdots</var> <var>A_{N-1}</var>\r\n')
        self.assertEqual(data.memory_limit_byte, 1024 * 1000 * 1000)
        self.assertEqual(data.name, 'Do Not Duplicate')
        self.assertEqual(data.problem, AtCoderProblem.from_url(url))
        self.assertEqual(data.sample_cases, [
            TestCase(name='sample-1', input_name='入力例 1', input_data=b'3 2\n1 2 3\n', output_name='出力例 1', output_data=b'2 3\n'),
            TestCase(name='sample-2', input_name='入力例 2', input_data=b'5 10\n1 2 3 2 3\n', output_name='出力例 2', output_data=b'3\n'),
            TestCase(name='sample-3', input_name='入力例 3', input_data=b'6 1000000000000\n1 1 2 2 3 3\n', output_name='出力例 3', output_data=b'\n'),
            TestCase(name='sample-4', input_name='入力例 4', input_data=b'11 97\n3 1 4 1 5 9 2 6 5 3 5\n', output_name='出力例 4', output_data=b'9 2 6\n'),
        ])
        self.assertEqual(data.score, 700)
        self.assertEqual(data.time_limit_msec, 2 * 1000)

    def test_from_html_without_sample_cases(self):
        url = 'https://atcoder.jp/contests/tenka1-2013-quala/tasks/tenka1_2013_qualA_a'
        resp = requests.get(url)
        html = resp.content.decode(resp.apparent_encoding)
        data = AtCoderProblemDetailedData.from_html(html, problem=AtCoderProblem.from_url(url))

        self.assertEqual(data.alphabet, 'A')
        self.assertEqual(data.available_languages, None)
        self.assertEqual(data.html, html)
        self.assertEqual(data.input_format, None)
        self.assertEqual(data.memory_limit_byte, 64 * 1000 * 1000)
        self.assertEqual(data.name, '天下一株式会社採用情報')
        self.assertEqual(data.problem, AtCoderProblem.from_url(url))
        self.assertEqual(data.sample_cases, [])
        self.assertEqual(data.score, None)
        self.assertEqual(data.time_limit_msec, 2 * 1000)

    def test_from_html_issue_414(self):
        url = 'https://atcoder.jp/contests/fuka5/tasks/fuka_graphcut'
        resp = requests.get(url)
        html = resp.content.decode(resp.apparent_encoding)
        data = AtCoderProblemDetailedData.from_html(html, problem=AtCoderProblem.from_url(url))

        self.assertEqual(data.alphabet, 'G')
        self.assertEqual(data.available_languages, None)
        self.assertEqual(data.html, html)
        self.assertEqual(data.input_format, None)
        self.assertEqual(data.memory_limit_byte, 256 * 1000 * 1000)
        self.assertEqual(data.name, 'Graph Cut')
        self.assertEqual(data.problem, AtCoderProblem.from_url(url))
        self.assertEqual(data.sample_cases, [
            TestCase(name='sample-1', input_name='Sample Input', input_data=b'10 10 0.4000 0.20\n\
.##...###.\n\
.##.####..\n\
.######...\n\
.#.#.####.\n\
######....\n\
##.##.....\n\
....#.....\n\
..####.#..\n\
.#####.##.\n\
.#####.##.\n\
25 38 0.5 0.24\n\
...........#...............#..........\n\
...........###..........####..........\n\
....##.....#####.......####...........\n\
.....##.....###############.....##....\n\
............#####.###.#####......#....\n\
............#########.####............\n\
.....##......#########.###............\n\
....##......#####.#########........#..\n\
....#......##.##..####..####..........\n\
.......#...###########.#####...#......\n\
.......##.##################..##......\n\
........#####.####.##.######.##.......\n\
..........####################........\n\
.........##.##..########..#####.......\n\
.......######....##..#....###.##......\n\
......###.####...##.##..#####.##.#....\n\
....###..##..#...#####..#..########...\n\
..####..###.....#######......#######..\n\
...#######......#######........###....\n\
..####.........##.######........###...\n\
...............###...###..............\n\
..............#######..#...#...##.....\n\
.........#....##########...#....#.....\n\
..#.....##.....########...............\n\
...............########...............\n\
0 0 0 0\n', output_name='Sample Output', output_data=b'11.200000\n\
.##...###.\n\
.##.####..\n\
.######...\n\
.######...\n\
######....\n\
##.##.....\n\
....#.....\n\
..####....\n\
.#####.##.\n\
.#####.##.\n\
73.540000\n\
...........#...............#..........\n\
...........###..........####..........\n\
...........#####.......####...........\n\
............###############...........\n\
............###############...........\n\
............##############............\n\
.............#############............\n\
............###############...........\n\
...........#################..........\n\
.......#...#################...#......\n\
.......##.##################..##......\n\
........####################.##.......\n\
..........####################........\n\
.........#####..########..#####.......\n\
.......######....#####....######......\n\
......########...#####..########.#....\n\
....#######..#...#####..#..########...\n\
..#########.....#######......#######..\n\
...#######......#######........###....\n\
..####.........#########........###...\n\
...............#########..............\n\
..............##########..............\n\
..............##########..............\n\
...............########...............\n\
...............########...............\n'),
        ])
        self.assertEqual(data.score, None)
        self.assertEqual(data.time_limit_msec, 5 * 1000)

    def test_download_sample_cases_pre_without_prettyprint_insection(self):
        # see: https://github.com/kmyk/online-judge-tools/issues/625
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/tdpc/tasks/tdpc_fibonacci').download_sample_cases(), [
            TestCase(name='sample-1', input_name='Sample Input 1', input_data=b'2 10\n', output_name='Sample Output 1', output_data=b'55\n'),
            TestCase(name='sample-2', input_name='Sample Input 2', input_data=b'3 10\n', output_name='Sample Output 2', output_data=b'105\n'),
        ])

    def test_download_sample_cases_s8pc_broken_html(self):
        # see: https://github.com/kmyk/online-judge-tools/issues/615
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/s8pc-4/tasks/s8pc_4_d').download_sample_cases(), [
            TestCase(name='sample-1', input_name='Sample Input 1', input_data=b'4\n1 2\n2 3\n2 4\n', output_name='Sample Output 1', output_data=b'2.0\n1.0\n2.0\n2.0\n'),
            TestCase(name='sample-2', input_name='Sample Input 2', input_data=b'4\n1 2\n2 4\n4 3\n', output_name='Sample Output 2', output_data=b'3.0\n1.5\n3.0\n1.5\n'),
            TestCase(name='sample-3', input_name='Sample Input 3', input_data=b'5\n1 2\n2 3\n3 4\n4 5\n', output_name='Sample Output 3', output_data=b'4.0\n2.0\n2.0\n2.0\n4.0\n'),
            TestCase(name='sample-4', input_name='Sample Input 4', input_data=b'7\n1 2\n1 3\n2 4\n2 5\n3 6\n3 7\n', output_name='Sample Output 4', output_data=b'2.000000000000\n1.666666666667\n1.666666666667\n3.000000000000\n3.000000000000\n3.000000000000\n3.000000000000\n'),
            TestCase(name='sample-5', input_name='Sample Input 5', input_data=b'12\n1 2\n2 3\n2 4\n4 5\n5 6\n5 7\n6 8\n8 9\n2 10\n10 11\n11 12\n', output_name='Sample Output 5', output_data=b'3.666666666667\n2.250000000000\n3.666666666667\n2.833333333333\n2.555555555556\n2.666666666667\n4.333333333333\n2.666666666667\n5.333333333333\n2.500000000000\n2.500000000000\n5.000000000000\n'),
            TestCase(name='sample-6', input_name='Sample Input 6', input_data=b'2\n1 2\n', output_name='Sample Output 6', output_data=b'1.0\n1.0\n'),
        ])

    @unittest.expectedFailure
    def test_download_sample_cases_ttpc2015_inserted_p_tag(self):
        # see: https://github.com/kmyk/online-judge-tools/pull/724
        # see: https://github.com/kmyk/online-judge-tools/issues/726
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/ttpc2015/tasks/ttpc2015_i').download_sample_cases(), [
            TestCase(name='sample-1', input_name='入力例1', input_data=b'5\n4 2 3 1 5\n', output_name='出力例1', output_data=b'3\n2 4\n1 2\n2 4\n'),
        ])


class AtCoderProblemGetInputFormatTest(unittest.TestCase):
    def test_normal(self):
        """
        .. code-block:: html

            <div class="io-style">
                <div class="part">
                    <section>
                        <h3>入力</h3>
                        <p>入力は以下の形式で標準入力から与えられる。</p>
                        <pre>
                            <var>N</var>
                        </pre>
                    </section>
                </div>
                <div class="part">
                    ...
                </div>
                ...
            </div>
        """

        self.assertEqual(AtCoderProblem.from_url('https://beta.atcoder.jp/contests/agc001/tasks/agc001_d').download_data().input_format, '<var>N</var> <var>M</var>\r\n<var>A_1</var> <var>A_2</var> <var>...</var> <var>A_M</var>\r\n')
        self.assertEqual(AtCoderProblem.from_url('https://beta.atcoder.jp/contests/agc002/tasks/agc002_d').download_data().input_format, '\r\n<var>N</var> <var>M</var>\r\n<var>a_1</var> <var>b_1</var>\r\n<var>a_2</var> <var>b_2</var>\r\n<var>:</var>\r\n<var>a_M</var> <var>b_M</var>\r\n<var>Q</var>\r\n<var>x_1</var> <var>y_1</var> <var>z_1</var>\r\n<var>x_2</var> <var>y_2</var> <var>z_2</var>\r\n<var>:</var>\r\n<var>x_Q</var> <var>y_Q</var> <var>z_Q</var>\r\n')
        self.assertEqual(AtCoderProblem.from_url('https://beta.atcoder.jp/contests/agc003/tasks/agc003_d').download_data().input_format, '<var>N</var>\r\n<var>s_1</var>\r\n:\r\n<var>s_N</var>\r\n')
        self.assertEqual(AtCoderProblem.from_url('https://beta.atcoder.jp/contests/agc004/tasks/agc004_d').download_data().input_format, '<var>N</var> <var>K</var>\r\n<var>a_1</var> <var>a_2</var> <var>...</var> <var>a_N</var>\r\n')
        self.assertEqual(AtCoderProblem.from_url('https://beta.atcoder.jp/contests/agc005/tasks/agc005_d').download_data().input_format, '<var>N</var> <var>K</var>\r\n')

        self.assertEqual(AtCoderProblem.from_url('https://beta.atcoder.jp/contests/arc083/tasks/arc083_a').download_data().input_format, '<var>A</var> <var>B</var> <var>C</var> <var>D</var> <var>E</var> <var>F</var>\r\n')

    def test_old_problem(self):
        """
        :note: https://github.com/kmyk/online-judge-tools/issues/380

        .. code-block:: html

            <h3>入力</h3>
            <section>
                入力は以下の形式で与えられる。
                <pre>
                    <var>N</var>
                </pre>
            </section>
        """

        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/arc001/tasks/arc001_1').download_data().input_format, '\r\n<var>N</var>\r\n<var>c_1c_2c_3…c_N</var>\r\n')
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/arc002/tasks/arc002_3').download_data().input_format, '\r\n<var>N</var>\r\n<var>c_{1}c_{2}...c_{N}</var>\r\n')
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/arc034/tasks/arc034_4').download_data().input_format, '\r\n<var>A</var> <var>B</var> <var>C</var>\r\n<var>a_1</var> <var>a_2</var> .. <var>a_A</var>\r\n<var>b_1</var> <var>b_2</var> .. <var>b_B</var>\r\n')

    def test_dwacon_problem(self):
        """
        :note: https://github.com/kmyk/online-judge-tools/issues/142

        .. code-block:: html

            <h3 id="入力">入力</h3>
            <p>入力は以下の形式で標準入力から与えられる。</p>
            <div class="io-style">
                <pre>
                    <var>N</var>
                </pre>
            </div>
        """

        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/dwacon2018-final/tasks/dwacon2018_final_a').download_data().input_format, '\r\n<var>H</var> <var>M</var> <var>S</var>\r\n<var>C_1</var> <var>C_2</var>\r\n')
        self.assertEqual(AtCoderProblem.from_url('https://atcoder.jp/contests/dwacon2018-final/tasks/dwacon2018_final_b').download_data().input_format, '\r\n<var>N</var> <var>K</var>\r\n<var>v_1</var> <var>...</var> <var>v_N</var>\r\n')

    def test_problem_without_input(self):
        self.assertIsNone(AtCoderProblem.from_url('https://atcoder.jp/contests/tenka1-2013-quala/tasks/tenka1_2013_qualA_a').download_data().input_format)

    def test_problem_without_input_format(self):
        self.assertIsNone(AtCoderProblem.from_url('https://atcoder.jp/contests/joi2006ho/tasks/joi2006ho_a').download_data().input_format)


if __name__ == '__main__':
    unittest.main()
