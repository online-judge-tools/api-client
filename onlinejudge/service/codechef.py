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


class CodeChefProblem(onlinejudge.type.Problem):
    def __init__(self, *, contest_id: str, problem_id: str):
        self.contest_id = contest_id
        self.problem_id = problem_id

    # TODO: support problems with old formats
    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[onlinejudge.type.TestCase]:
        session = session or utils.get_default_session()

        # get
        url = 'https://www.codechef.com/api/contests/{}/problems/{}'.format(self.contest_id, self.problem_id)
        resp = utils.request('GET', url, session=session)
        data = json.loads(resp.content)
        if data['status'] != 'success':
            logger.debug('json: %s', resp.content.decode())
            raise SampleParseError('CodeChef API failed with: {}'.format(data.get('message')))

        # convert
        testcases: List[onlinejudge.type.TestCase] = []
        for testcase in data['problemComponents']['sampleTestCases']:
            testcases.append(onlinejudge.type.TestCase(
                name='sample-{}'.format(testcase['id']),
                input_name='input',
                input_data=utils.textfile(testcase['input']).encode(),
                output_name='output',
                output_data=utils.textfile(testcase['output']).encode(),
            ))
        return testcases

    def get_url(self, *, contests: bool = True) -> str:
        return 'https://www.codechef.com/{}/problems/{}'.format(self.contest_id, self.problem_id)

    def get_service(self) -> CodeChefService:
        return CodeChefService()

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
onlinejudge.dispatch.problems += [CodeChefProblem]
