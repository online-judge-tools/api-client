# Python Version: 3.x
# -*- coding: utf-8 -*-
"""
the module for Facebook Hacker Cup (https://www.facebook.com/hackercup/)

.. versionadded:: 6.5.0
"""

import json
import urllib.parse
from logging import getLogger
from typing import *

import requests

import onlinejudge._implementation.utils as utils
import onlinejudge.type
from onlinejudge.type import TestCase

logger = getLogger(__name__)


class FacebookHackerCupService(onlinejudge.type.Service):
    def get_url(self) -> str:
        return 'https://www.facebook.com/hackercup/'

    def get_name(self) -> str:
        return 'Facebook Hacker Cup'

    @classmethod
    def from_url(cls, url: str) -> Optional['FacebookHackerCupService']:
        # old format
        # example: https://www.facebook.com/hackercup/
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'www.facebook.com' \
                and utils.normpath(result.path).startswith('/hackercup'):
            return cls()

        # new format
        # example: https://www.facebook.com/codingcompetitions/
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'www.facebook.com' \
                and utils.normpath(result.path).startswith('/codingcompetitions'):
            return cls()
        return None


class FacebookHackerCupProblem(onlinejudge.type.Problem):
    """
    :ivar series_vanity: :py:class:`str`
    :ivar season_vanity: :py:class:`str`
    :ivar contest_vanity: :py:class:`str`
    :ivar display_index: :py:class:`str`

    .. versionchanged:: 10.4.0
    """
    def __init__(self, *, series_vanity: str, season_vanity: str, contest_vanity: str, display_index: str):
        self.series_vanity = series_vanity
        self.season_vanity = season_vanity
        self.contest_vanity = contest_vanity
        self.display_index = display_index

    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[TestCase]:
        session = session or utils.get_default_session()
        url = 'https://www.facebook.com/api/graphql/'

        # get problem_id
        data = {
            'fb_api_req_friendly_name': 'CodingCompetitionsContestRootQuery',
            'variables': json.dumps({
                "series_vanity": self.series_vanity,
                "season_vanity": self.season_vanity,
                "contest_vanity": self.contest_vanity,
            }),
            'doc_id': '2709858395781426',
        }  # type: Dict[str, Any]
        resp = utils.request('POST', url, session=session, data=data)
        try:
            result = json.loads(resp.content.decode())  # type: Dict[str, Any]
        except json.decoder.JSONDecodeError as e:
            raise onlinejudge.type.SampleParseError("The result of Facebook's API is empty. Did you set your User-Agent?") from e
        contest_id = result['data']['contestSeries']['contestSeason']['contest']['id']

        # get sample URLs
        data = {
            'fb_api_req_friendly_name': 'CodingCompetitionsContestProblemQuery',
            'variables': json.dumps({
                "contest_id": contest_id,
                "series_vanity": self.series_vanity,
                "display_index": self.display_index,
                "participation_type": "UNTIMED_PRACTICE",
                "can_submit": False,
            }),
            'doc_id': '3556774947707941',
        }
        resp = utils.request('POST', url, session=session, data=data)
        result = json.loads(resp.content.decode())
        problem_sample_test_case_set = result['data']['contest']['problem']['problem_sample_test_case_set']

        # return the result
        sample = TestCase(
            'sample',
            'Sample Input',
            problem_sample_test_case_set['test_case_set_full_input'].encode(),
            'Sample Output',
            problem_sample_test_case_set['test_case_set_full_output'].encode(),
        )
        return [sample]

    def get_url(self) -> str:
        return 'https://www.facebook.com/codingcompetitions/{}/{}/{}/problems/{}'.format(self.series_vanity, self.season_vanity, self.contest_vanity, self.display_index)

    @classmethod
    def from_url(cls, url: str) -> Optional['FacebookHackerCupProblem']:
        # removed format
        # example: https://www.facebook.com/hackercup/problem/448364075989193/
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'www.facebook.com' \
                and utils.normpath(result.path).startswith('/hackercup/problem/'):
            dirs = utils.normpath(result.path).split('/')
            if len(dirs) > 3 and dirs[3].isdigit():
                logger.warning('The old platform of Facebook Hacker Cup has been replaced. See https://github.com/online-judge-tools/api-client/issues/84')

        # new format
        # example: https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/A
        dirs = utils.normpath(result.path).split('/')
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'www.facebook.com' \
                and len(dirs) >= 7 and dirs[1] == 'codingcompetitions' and dirs[5] == 'problems':
            return cls(
                series_vanity=dirs[2],
                season_vanity=dirs[3],
                contest_vanity=dirs[4],
                display_index=dirs[6],
            )
        return None

    def get_service(self) -> FacebookHackerCupService:
        return FacebookHackerCupService()


onlinejudge.dispatch.services += [FacebookHackerCupService]
onlinejudge.dispatch.problems += [FacebookHackerCupProblem]
