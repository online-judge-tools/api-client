# Python Version: 3.x
# -*- coding: utf-8 -*-
"""
the module for Algo-Method (https://algo-method.com/)
"""

import json
import posixpath
import re
import urllib.parse
from typing import *

import bs4
import requests

import onlinejudge._implementation.testcase_zipper
import onlinejudge._implementation.utils as utils
import onlinejudge.dispatch
import onlinejudge.type


class AlgoMethodService(onlinejudge.type.Service):
    def get_url(self) -> str:
        return 'https://algo-method.com/'

    def get_name(self) -> str:
        return 'algo-method'

    @classmethod
    def from_url(cls, url: str) -> Optional['AlgoMethodService']:
        # example: https://algo-method.com/
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'algo-method.com':
            return cls()
        return None


class AlgoMethodProblem(onlinejudge.type.Problem):
    def __init__(self, *, problem_id: str):
        self.problem_id = problem_id

    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[onlinejudge.type.TestCase]:
        session = session or utils.get_default_session()
        # get
        resp = utils.request('GET', self.get_url(), session=session)
        # parse
        soup = bs4.BeautifulSoup(resp.text, utils.HTML_PARSER)
        samples = onlinejudge._implementation.testcase_zipper.SampleZipper()
        for case, name in self._parse_sample_cases(soup):
            samples.add(case.encode(), name)
        return samples.get()

    def _parse_sample_cases(self, soup: bs4.BeautifulSoup) -> Generator[Tuple[str, str], None, None]:
        body_md = json.loads(soup.find(id='__NEXT_DATA__').get_text())['props']['pageProps']['tasks']['body']
        pattern = r'#### ([入出]力例 \d ?)\r\n```IOExample\r\n([\s\S]+?)```'
        cases = re.findall(pattern, body_md)
        for name, case in cases:
            yield (utils.dos2unix(case), name)

    def get_url(self) -> str:
        return 'https://algo-method.com/tasks/{}'.format(self.problem_id)

    def get_service(self) -> AlgoMethodService:
        return AlgoMethodService()

    @classmethod
    def from_url(cls, url: str) -> Optional['AlgoMethodProblem']:
        # example: https://algo-method.com/tasks/15
        result = urllib.parse.urlparse(url)
        dirname, basename = posixpath.split(utils.normpath(result.path))
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'algo-method.com' \
                and dirname == '/tasks' \
                and basename:
            return cls(problem_id=basename)
        return None


onlinejudge.dispatch.services += [AlgoMethodService]
onlinejudge.dispatch.problems += [AlgoMethodProblem]
