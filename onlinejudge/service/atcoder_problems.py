"""
the module for virtual contests in AtCoder Problems (https://kenkoooo.com/atcoder/#/contest/recent)
"""

import json
import re
import urllib.parse
from logging import getLogger
from typing import *

import onlinejudge._implementation.utils as utils
import onlinejudge.dispatch
import onlinejudge.type
from onlinejudge.service.atcoder import AtCoderProblem, AtCoderService
from onlinejudge.type import *

logger = getLogger(__name__)


class AtCoderProblemsContest(onlinejudge.type.Contest):
    """
    :ivar contest_id: :py:class:`str`
    """
    def __init__(self, *, contest_id: str):
        self.contest_id = contest_id

    def get_url(self) -> str:
        return 'https://kenkoooo.com/atcoder/#/contest/show/{}'.format(self.contest_id)

    @classmethod
    def from_url(cls, url: str) -> Optional['AtCoderProblemsContest']:
        """
        :param url: example:

        -   https://kenkoooo.com/atcoder/#/contest/show/a7ac9c74-47ad-4166-9553-41a82b749a37
        """

        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'kenkoooo.com' \
                and result.path.startswith('/atcoder'):
            paths = result.fragment.split('/')
            if len(paths) >= 4 and paths[0] == '' and paths[1] == 'contest' and paths[2] == 'show' and re.match(r'^[-0-9a-f]+$', paths[3]):
                return cls(contest_id=paths[3])
        return None

    def get_service(self) -> AtCoderService:
        return AtCoderService()

    def _download_data(self, *, session: Optional[requests.Session] = None) -> Dict[str, Any]:
        session = session or utils.get_default_session()

        # prepare merged-problems.json
        url = 'https://kenkoooo.com/atcoder/resources/merged-problems.json'
        resp = utils.request('GET', url, session=session)
        problems = json.loads(resp.content)
        problem_dict = {problem['id']: problem for problem in problems}

        # call the internal API
        url = 'https://kenkoooo.com/atcoder/internal-api/contest/get/{}'.format(self.contest_id)
        resp = utils.request('GET', url, session=session)
        data = json.loads(resp.content)

        # make result
        result = {
            'url': self.get_url(),
            'name': data['info']['title'],
            'problems': [],
            'raw': resp.content.decode(),
        }
        for problem in data['problems']:
            result['problems'].append({
                'url': AtCoderProblem(problem_id=problem['id'], contest_id=problem_dict[problem['id']]['contest_id']).get_url(),
                'name': problem_dict[problem['id']]['title'],
                'context': {
                    'contest': {
                        'url': self.get_url(),
                        'name': data['info']['title'],
                    },
                    'alphabet': str(problem['order']),
                },
            })
        return result

    def list_problems(self, *, session: Optional[requests.Session] = None) -> Sequence[AtCoderProblem]:
        data = self._download_data(session=session)
        problems = []
        for problem in data['problems']:
            problem_ = AtCoderProblem.from_url(problem['url'])
            assert problem_  # for mypy
            problems.append(problem_)
        return problems


onlinejudge.dispatch.contests += [AtCoderProblemsContest]
