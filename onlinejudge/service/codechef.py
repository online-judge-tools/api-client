# Python Version: 3.x
"""
the module for CodeChef (https://www.codechef.com/)
"""

import json
import re
import urllib.parse
from logging import getLogger
from typing import *

import requests

import onlinejudge._implementation.testcase_zipper
import onlinejudge._implementation.utils as utils
import onlinejudge.dispatch
import onlinejudge.type
from onlinejudge.type import SampleParseError

logger = getLogger(__name__)


class CodeChefService(onlinejudge.type.Service):
    def get_url(self) -> str:
        return 'https://www.codechef.com/'

    def get_name(self) -> str:
        return 'CodeChef'

    @classmethod
    def from_url(cls, url: str) -> Optional['CodeChefService']:
        # example: https://www.codechef.com/
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'www.codechef.com':
            return cls()
        return None

    def get_url_of_login_page(self) -> str:
        return 'https://www.codechef.com/'

    def is_logged_in(self, *, session: Optional[requests.Session] = None) -> bool:
        session = session or utils.get_default_session()
        url = 'https://www.codechef.com/certificates/'
        resp = utils.request('GET', url, session=session, raise_for_status=False)
        return resp.status_code == 200


class CodeChefProblemData(onlinejudge.type.ProblemData):
    def __init__(self, *, contest_id: str, data: Dict[str, Any]):
        self.contest_id = contest_id
        self.data = data

    @property
    def json(self) -> bytes:
        return json.dumps(self.data).encode()

    @property
    def problem(self) -> 'CodeChefProblem':
        return CodeChefProblem(contest_id=self.contest_id, problem_id=self.data['code'])

    @property
    def name(self) -> str:
        return self.data['name']

    # TODO: Support problems with old formats. Our old parser may help it: https://github.com/online-judge-tools/api-client/pull/50/commits/a6c2c0808bc2b5ef5c81985877522b8e8ea92bd1
    @property
    def sample_cases(self) -> Optional[List[onlinejudge.type.TestCase]]:
        if 'problemComponents' not in self.data:
            return None
        testcases: List[onlinejudge.type.TestCase] = []
        for testcase in self.data['problemComponents']['sampleTestCases']:
            testcases.append(onlinejudge.type.TestCase(
                name='sample-{}'.format(testcase['id']),
                input_name='input',
                input_data=utils.textfile(testcase['input']).encode(),
                output_name='output',
                output_data=utils.textfile(testcase['output']).encode(),
            ))
        return testcases


class CodeChefContestData(onlinejudge.type.ContestData):
    def __init__(self, *, data: Dict[str, Any]):
        self.data = data

    @property
    def json(self) -> bytes:
        return json.dumps(self.data).encode()

    @property
    def contest(self) -> 'CodeChefContest':
        return CodeChefContest(contest_id=self.data['code'])

    @property
    def name(self) -> str:
        return self.data['name']

    def get_problem_data(self) -> List['CodeChefProblemData']:
        return [CodeChefProblemData(contest_id=self.data['code'], data=data) for data in self.data['problems'].values()]


class CodeChefContest(onlinejudge.type.Contest):
    def __init__(self, *, contest_id: str):
        self.contest_id = contest_id

    def get_url(self) -> str:
        return 'https://www.codechef.com/{}'.format(self.contest_id)

    def get_service(self) -> CodeChefService:
        return CodeChefService()

    @classmethod
    def from_url(cls, url: str) -> Optional['CodeChefContest']:
        # example: https://www.codechef.com/JAN20A
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'www.codechef.com':
            m = re.match(r'/([0-9A-Z_a-z-]+)', result.path)
            if m:
                contest_id = m.group(1)
                return cls(contest_id=contest_id)
        return None

    def list_problems(self, *, session: Optional[requests.Session] = None) -> Sequence['CodeChefProblem']:
        return [problem_data.problem for problem_data in self.download_data(session=session).get_problem_data()]

    def download_data(self, *, session: Optional[requests.Session] = None) -> CodeChefContestData:
        session = session or utils.get_default_session()

        # get
        url = 'https://www.codechef.com/api/contests/{}'.format(self.contest_id)
        resp = utils.request('GET', url, session=session)
        data = json.loads(resp.content)
        if data['status'] != 'success':
            logger.debug('json: %s', resp.content.decode())
            raise SampleParseError('CodeChef API failed with: {}'.format(data.get('message')))

        return CodeChefContestData(data=data)


class CodeChefProblem(onlinejudge.type.Problem):
    def __init__(self, *, contest_id: str, problem_id: str):
        self.contest_id = contest_id
        self.problem_id = problem_id

    def download_data(self, *, session: Optional[requests.Session] = None) -> CodeChefProblemData:
        session = session or utils.get_default_session()

        # get
        url = 'https://www.codechef.com/api/contests/{}/problems/{}'.format(self.contest_id, self.problem_id)
        resp = utils.request('GET', url, session=session)
        data = json.loads(resp.content)
        if data['status'] != 'success':
            logger.debug('json: %s', resp.content.decode())
            raise SampleParseError('CodeChef API failed with: {}'.format(data.get('message')))

        return CodeChefProblemData(contest_id=self.contest_id, data=data)

    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[onlinejudge.type.TestCase]:
        sample_cases = self.download_data(session=session).sample_cases
        assert sample_cases is not None
        return sample_cases

    def get_url(self, *, contests: bool = True) -> str:
        return 'https://www.codechef.com/{}/problems/{}'.format(self.contest_id, self.problem_id)

    def get_service(self) -> CodeChefService:
        return CodeChefService()

    def get_contest(self) -> CodeChefContest:
        return CodeChefContest(contest_id=self.contest_id)

    @classmethod
    def from_url(cls, url: str) -> Optional['CodeChefProblem']:
        # example: https://www.codechef.com/JAN20A/problems/DYNAMO
        # example: https://www.codechef.com/JAN20A/submit/DYNAMO
        # example: https://www.codechef.com/JAN20A/status/DYNAMO
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'www.codechef.com':
            m = re.match(r'/([0-9A-Z_a-z-]+)/(?:problems|submit|status)/([0-9A-Z_a-z-]+)/?', result.path)
            if m:
                contest_id = m.group(1)
                problem_id = m.group(2)
                return cls(problem_id=problem_id, contest_id=contest_id)
        return None


onlinejudge.dispatch.services += [CodeChefService]
onlinejudge.dispatch.contests += [CodeChefContest]
onlinejudge.dispatch.problems += [CodeChefProblem]
