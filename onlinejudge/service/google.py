"""
the module for Google Code Jam and Google Kick Start (https://codingcompetitions.withgoogle.com/)

.. versionadded:: 9.2.0
"""

import base64
import json
import re
import string
import urllib.parse
from itertools import islice
from logging import getLogger
from typing import *

import bs4
import requests

import onlinejudge._implementation.utils as utils
import onlinejudge.type
from onlinejudge.type import SampleParseError, TestCase

logger = getLogger(__name__)


class GoogleCodeJamService(onlinejudge.type.Service):
    def get_url(self) -> str:
        return 'https://codingcompetitions.withgoogle.com/'

    def get_name(self) -> str:
        return 'Google Code Jam'

    @classmethod
    def from_url(cls, url: str) -> Optional['GoogleCodeJamService']:
        # example: https://codingcompetitions.withgoogle.com/
        # example: https://code.google.com/codejam
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https'):
            if result.netloc == 'codingcompetitions.withgoogle.com':
                return cls()
            if result.netloc == 'code.google.com':
                dirs = utils.normpath(result.path).split('/')
                if len(dirs) >= 2 and dirs[1] == 'codejam':
                    return cls()
        return None


class GoogleCodeJamProblem(onlinejudge.type.Problem):
    """
    :ivar domain: :py:class:`str`, this must be `codingcompetitions.withgoogle.com` or `code.google.com`
    :ivar kind: :py:class:`str`, this is typically `codejam` or `kickstart`
    :ivar contest_id: :py:class:`str`
    :ivar problem_id: :py:class:`str`
    """
    def __init__(self, *, domain: str, kind: str, contest_id: str, problem_id: str):
        assert domain in ('codingcompetitions.withgoogle.com', 'code.google.com')
        self.domain = domain
        self.kind = kind
        self.contest_id = contest_id
        self.problem_id = problem_id

    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[TestCase]:
        session = session or utils.get_default_session()
        if self.domain == 'codingcompetitions.withgoogle.com':
            url = 'https://codejam.googleapis.com/dashboard/{}/poll?p=e30'.format(self.contest_id)
            resp = utils.request('GET', url, session=session)
            data = json.loads(base64.urlsafe_b64decode(resp.content + b'=' * ((-len(resp.content)) % 4)).decode())
            logger.debug('%s', data)

            # parse JSON
            for task in data['challenge']['tasks']:
                if task['id'] == self.problem_id:
                    statement = task['statement']
                    break
            else:
                raise SampleParseError("the problem {} is not found in the challenge {}".format(repr(self.problem_id), repr(self.contest_id)))

        elif self.domain == 'code.google.com':
            try:
                url = 'https://{}/{}/contest/{}/dashboard/ContestInfo'.format(self.domain, self.kind, self.contest_id)
                resp = utils.request('GET', url, session=session)
            except requests.HTTPError:
                logger.warning('hint: Google Code Jam moves old problems to the new platform')
                raise
            data = json.loads(resp.content.decode())

            # parse JSON
            assert self.problem_id.startswith('p')
            i = int(self.problem_id[1:])
            statement = data['problems'][i]['body']

        else:
            assert False

        # parse HTML
        soup = bs4.BeautifulSoup(statement, utils.HTML_PARSER)
        io_contents = soup.find_all('pre', class_='io-content')
        if len(io_contents) % 2 != 0:
            raise SampleParseError("""the number of <pre class="io-content"> is not multiple of two""")

        input_contents = islice(io_contents, 0, None, 2)
        output_contents = islice(io_contents, 1, None, 2)

        samples = []

        for index, (input_content, output_content) in enumerate(zip(input_contents, output_contents)):
            if input_content.text.startswith('Case #'):
                logger.warning('''the sample input starts with "Case #"''')
            if not output_content.text.startswith('Case #'):
                logger.warning('''the sample output doesn't start with "Case #"''')
            samples.append(TestCase(
                'sample-{}'.format(index + 1),
                'Input {}'.format(index + 1),
                utils.textfile(input_content.text.rstrip()).encode(),
                'Output {}'.format(index + 1),
                utils.textfile(output_content.text.rstrip()).encode(),
            ))

        return samples

    def get_url(self) -> str:
        if self.domain == 'codingcompetitions.withgoogle.com':
            return 'https://{}/{}/round/{}/{}'.format(self.domain, self.kind, self.contest_id, self.problem_id)
        elif self.domain == 'code.google.com':
            return 'https://{}/{}/contest/{}/dashboard#s={}'.format(self.domain, self.kind, self.contest_id, self.problem_id)
        else:
            assert False

    @classmethod
    def from_url(cls, url: str) -> Optional['GoogleCodeJamProblem']:
        # example: https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/000000000020993c
        # example: https://codingcompetitions.withgoogle.com/kickstart/round/000000000019ffc7/00000000001d3f56
        # example: https://code.google.com/codejam/contest/7234486/dashboard
        # example: https://code.google.com/codejam/contest/7234486/dashboard#s=p0
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https'):
            dirs = utils.normpath(result.path).split('/')
            if result.netloc == 'codingcompetitions.withgoogle.com':
                if len(dirs) >= 5 and dirs[2] == 'round' and all(c in string.hexdigits for c in dirs[3]) and all(c in string.hexdigits for c in dirs[4]):
                    return cls(domain=result.netloc, kind=dirs[1], contest_id=dirs[3], problem_id=dirs[4])
            if result.netloc == 'code.google.com':
                if len(dirs) >= 5 and dirs[2] == 'contest' and dirs[3].isdigit() and dirs[4] == 'dashboard':
                    if result.fragment == '' or re.match(r'^s=p\d+$', result.fragment):
                        problem_id = (result.fragment or 's=p0')[2:]
                        return cls(domain=result.netloc, kind=dirs[1], contest_id=dirs[3], problem_id=problem_id)
        return None

    def get_service(self) -> GoogleCodeJamService:
        return GoogleCodeJamService()


onlinejudge.dispatch.services += [GoogleCodeJamService]
onlinejudge.dispatch.problems += [GoogleCodeJamProblem]
