# Python Version: 3.x
# -*- coding: utf-8 -*-
"""
the module for Facebook Hacker Cup (https://www.facebook.com/hackercup/)

.. versionadded:: 6.5.0
"""

import urllib.parse
from typing import *

import requests

import onlinejudge._implementation.utils as utils
import onlinejudge.type
from onlinejudge.type import TestCase


class FacebookHackerCupService(onlinejudge.type.Service):
    def get_url(self) -> str:
        return 'https://www.facebook.com/hackercup/'

    def get_name(self) -> str:
        return 'Facebook Hacker Cup'

    @classmethod
    def from_url(cls, url: str) -> Optional['FacebookHackerCupService']:
        # example: https://www.facebook.com/hackercup/
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'www.facebook.com' \
                and utils.normpath(result.path).startswith('/hackercup'):
            return cls()
        return None


class FacebookHackerCupProblem(onlinejudge.type.Problem):
    """
    :ivar problem_id: :py:class:`int`
    """
    def __init__(self, *, problem_id: int):
        self.problem_id = problem_id

    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[TestCase]:
        raise NotImplementedError('The old platform of Facebook Hacker Cup has been replaced. See https://github.com/online-judge-tools/api-client/issues/84')

    def get_url(self) -> str:
        return 'https://www.facebook.com/hackercup/problem/{}/'.format(self.problem_id)

    @classmethod
    def from_url(cls, url: str) -> Optional['FacebookHackerCupProblem']:
        # example: https://www.facebook.com/hackercup/problem/448364075989193/
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'www.facebook.com' \
                and utils.normpath(result.path).startswith('/hackercup/problem/'):
            dirs = utils.normpath(result.path).split('/')
            if len(dirs) > 3 and dirs[3].isdigit():
                problem_id = int(dirs[3])
                return cls(problem_id=problem_id)
        return None

    def get_service(self) -> FacebookHackerCupService:
        return FacebookHackerCupService()


onlinejudge.dispatch.services += [FacebookHackerCupService]
onlinejudge.dispatch.problems += [FacebookHackerCupProblem]
