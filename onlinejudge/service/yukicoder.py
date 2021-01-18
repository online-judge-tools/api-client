# Python Version: 3.x
# -*- coding: utf-8 -*-
"""
the module for yukicoder (https://yukicoder.me/)

:note: There is the official API https://petstore.swagger.io/?url=https://yukicoder.me/api/swagger.yaml
"""

import json
import posixpath
import string
import urllib.parse
from logging import getLogger
from typing import *

import bs4

import onlinejudge._implementation.testcase_zipper
import onlinejudge._implementation.utils as utils
import onlinejudge.dispatch
from onlinejudge.type import *

logger = getLogger(__name__)


class YukicoderService(onlinejudge.type.Service):
    def get_url_of_login_page(self):
        return self.get_url()

    def is_logged_in(self, *, session: Optional[requests.Session] = None) -> bool:
        session = session or utils.get_default_session()
        url = 'https://yukicoder.me'
        resp = utils.request('GET', url, session=session)
        assert resp.status_code == 200
        return 'login-btn' not in str(resp.content)

    def get_url(self) -> str:
        return 'https://yukicoder.me/'

    def get_name(self) -> str:
        return 'yukicoder'

    @classmethod
    def from_url(cls, url: str) -> Optional['YukicoderService']:
        # example: http://yukicoder.me/
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'yukicoder.me':
            return cls()
        return None

    _problems = None

    @classmethod
    def _get_problems(cls, *, session: Optional[requests.Session] = None) -> List[Dict[str, Any]]:
        """`_get_problems` wraps the official API and caches the result.
        """

        session = session or utils.get_default_session()
        if cls._problems is None:
            url = 'https://yukicoder.me/api/v1/problems'
            resp = utils.request('GET', url, session=session)
            cls._problems = json.loads(resp.content.decode())
        return cls._problems

    _contests = None  # type: Optional[List[Dict[str, Any]]]

    @classmethod
    def _get_contests(cls, *, session: Optional[requests.Session] = None) -> List[Dict[str, Any]]:
        """`_get_contests` wraps the official API and caches the result.
        """

        session = session or utils.get_default_session()
        if cls._contests is None:
            cls._contests = []
            for tense in ('past', 'current', 'future'):
                url = 'https://yukicoder.me/api/v1/contest/{}'.format(tense)
                resp = utils.request('GET', url, session=session)
                cls._contests.extend(json.loads(resp.content.decode()))
        return cls._contests

    @classmethod
    def _get_csrf_token(cls, *, session: requests.Session) -> str:
        url = 'https://yukicoder.me/csrf_token'
        resp = utils.request('GET', url, session=session)
        return resp.content.decode()


class YukicoderContest(onlinejudge.type.Contest):
    """
    :ivar contest_id: :py:class:`int`

    .. versionadded:: 10.4.0
    """
    def __init__(self, *, contest_id: int):
        self.contest_id = contest_id

    def _download_data(self, *, session: Optional[requests.Session] = None) -> Dict[str, Any]:
        session = session or utils.get_default_session()

        url = 'https://yukicoder.me/api/v1/problems'
        resp = utils.request('GET', url, session=session)
        problems = json.loads(resp.content)
        problem_dict = {problem['ProblemId']: problem for problem in problems}

        url = 'https://yukicoder.me/api/v1/contest/id/{}'.format(self.contest_id)
        resp = utils.request('GET', url, session=session)
        data = json.loads(resp.content)

        result = {
            'url': self.get_url(),
            'name': data['Name'],
            'problems': [],
            'raw': resp.content.decode(),
        }
        for index, problem_id in enumerate(data['ProblemIdList']):
            if problem_id in problem_dict:
                name = problem_dict[problem_id]['Title']
            else:
                name = '問題名非公開'
            result['problems'].append({
                "url": YukicoderProblem(problem_id=problem_id).get_url(),
                "name": name,
                "context": {
                    "contest": {
                        "name": data['Name'],
                        "url": self.get_url(),
                    },
                    "alphabet": string.ascii_uppercase[index],
                },
            })
        return result

    def list_problems(self, *, session: Optional[requests.Session] = None) -> Sequence['YukicoderProblem']:
        """
        :raises RuntimeError:
        """

        session = session or utils.get_default_session()
        url = 'https://yukicoder.me/api/v1/contest/id/{}'.format(self.contest_id)
        resp = utils.request('GET', url, session=session)
        data = json.loads(resp.content.decode())
        return [YukicoderProblem(problem_id=problem_id) for problem_id in data['ProblemIdList']]

    def get_url(self) -> str:
        return 'https://yukicoder.me/contests/{}'.format(self.contest_id)

    def get_service(self) -> Service:
        return YukicoderService()

    @classmethod
    def from_url(cls, url: str) -> Optional['Contest']:
        # example: https://yukicoder.me/contests/276
        # example: http://yukicoder.me/contests/276/all
        result = urllib.parse.urlparse(url)
        dirs = utils.normpath(result.path).split('/')
        if result.scheme in ('', 'http', 'https') and result.netloc == 'yukicoder.me':
            if len(dirs) >= 3 and dirs[1] == 'contests':
                try:
                    contest_id = int(dirs[2])
                except ValueError:
                    pass
                else:
                    return cls(contest_id=contest_id)
        return None


class YukicoderProblem(onlinejudge.type.Problem):
    def __init__(self, *, problem_no=None, problem_id=None):
        assert problem_no or problem_id
        assert not problem_no or isinstance(problem_no, int)
        assert not problem_id or isinstance(problem_id, int)
        self.problem_no = problem_no
        self.problem_id = problem_id

    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[TestCase]:
        session = session or utils.get_default_session()
        # get
        resp = utils.request('GET', self.get_url(), session=session)
        # parse
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.HTML_PARSER)
        samples = onlinejudge._implementation.testcase_zipper.SampleZipper()
        for pre in soup.select('.sample pre'):
            logger.debug('pre: %s', str(pre))
            it = self._parse_sample_tag(pre)
            if it is not None:
                data, name = it
                samples.add(data.encode(), name)
        return samples.get()

    def download_system_cases(self, *, session: Optional[requests.Session] = None) -> List[TestCase]:
        """
        :raises NotLoggedInError:
        """

        session = session or utils.get_default_session()
        if not self.get_service().is_logged_in(session=session):
            raise NotLoggedInError
        url = '{}/testcase.zip'.format(self.get_url())
        resp = utils.request('GET', url, session=session)
        fmt = 'test_%e/%s'
        return onlinejudge._implementation.testcase_zipper.extract_from_zip(resp.content, fmt, ignore_unmatched_samples=True)  # NOTE: yukicoder's test sets sometimes contain garbages. The owner insists that this is an intended behavior, so we need to ignore them.

    def _parse_sample_tag(self, tag: bs4.Tag) -> Optional[Tuple[str, str]]:
        assert isinstance(tag, bs4.Tag)
        assert tag.name == 'pre'
        prv = utils.previous_sibling_tag(tag)
        pprv = tag.parent and utils.previous_sibling_tag(tag.parent)
        if prv.name == 'h6' and tag.parent.name == 'div' and tag.parent['class'] == ['paragraph'] and pprv.name == 'h5':
            logger.debug('h6: %s', str(prv))
            logger.debug('name.encode(): %s', prv.string.encode())

            s = utils.parse_content(tag)

            return utils.textfile(s.lstrip()), pprv.string + ' ' + prv.string
        return None

    def submit_code(self, code: bytes, language_id: LanguageId, *, filename: Optional[str] = None, session: Optional[requests.Session] = None) -> onlinejudge.type.Submission:
        """
        :raises NotLoggedInError:
        """

        # NOTE: An implementation with the official API exists at 492d8d7. This is reverted at 2b7e6f5 because the API ignores cookies and says "提出するにはログインが必要です" at least at that time.

        session = session or utils.get_default_session()
        # get
        url = self.get_url() + '/submit'
        resp = utils.request('GET', url, session=session)
        # parse
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.HTML_PARSER)
        form = soup.find('form', id='submit_form')
        if not form:
            logger.error('form not found')
            raise NotLoggedInError
        # post
        form = utils.FormSender(form, url=resp.url)
        form.set('lang', language_id)
        form.set_file('file', filename or 'code', code)
        form.unset('custom_test')
        resp = form.request(session=session)
        resp.raise_for_status()
        # result
        if 'submissions' in resp.url:
            # example: https://yukicoder.me/submissions/314087
            logger.info('success: result: %s', resp.url)
            return utils.DummySubmission(resp.url, problem=self)
        else:
            logger.error('failure')
            soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.HTML_PARSER)
            for div in soup.findAll('div', attrs={'role': 'alert'}):
                logger.warning('yukicoder says: "%s"', div.string)
            raise SubmissionError

    def get_available_languages(self, *, session: Optional[requests.Session] = None) -> List[Language]:
        session = session or utils.get_default_session()
        url = 'https://yukicoder.me/api/v1/languages'
        resp = utils.request('GET', url, session=session)
        data = json.loads(resp.content.decode())
        return [Language(language['Id'], language['Name'] + ' (' + language['Ver'] + ')') for language in data]

    def get_url(self) -> str:
        if self.problem_no:
            return 'https://yukicoder.me/problems/no/{}'.format(self.problem_no)
        elif self.problem_id:
            return 'https://yukicoder.me/problems/{}'.format(self.problem_id)
        else:
            raise ValueError

    @classmethod
    def from_url(cls, url: str) -> Optional['YukicoderProblem']:
        # example: https://yukicoder.me/problems/no/499
        # example: http://yukicoder.me/problems/1476
        result = urllib.parse.urlparse(url)
        dirname, basename = posixpath.split(utils.normpath(result.path))
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'yukicoder.me':
            n = None  # type: Optional[int]
            try:
                n = int(basename)
            except ValueError:
                pass
            if n is not None:
                if dirname == '/problems/no':
                    return cls(problem_no=n)
                if dirname == '/problems':
                    return cls(problem_id=n)
        return None

    def get_service(self) -> YukicoderService:
        return YukicoderService()

    def get_input_format(self, *, session: Optional[requests.Session] = None) -> Optional[str]:
        session = session or utils.get_default_session()
        # get
        resp = utils.request('GET', self.get_url(), session=session)
        # parse
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.HTML_PARSER)
        for h4 in soup.find_all('h4'):
            if h4.string == '入力':
                return h4.parent.find('pre').decode_contents(formatter=None)
        return None


onlinejudge.dispatch.services += [YukicoderService]
onlinejudge.dispatch.contests += [YukicoderContest]
onlinejudge.dispatch.problems += [YukicoderProblem]
