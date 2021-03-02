"""
the module for Kagamiz Contest System (https://kcs.miz-miz.biz/)
"""

import json
import urllib.parse
from logging import getLogger
from typing import *

import bs4
import requests

import onlinejudge._implementation.utils as utils
import onlinejudge.type
from onlinejudge.type import *

logger = getLogger(__name__)


class KagamizContestSystemService(onlinejudge.type.Service):
    def get_url(self) -> str:
        return 'https://kcs.miz-miz.biz/'

    def get_name(self) -> str:
        return 'Kagamiz Contest System'

    @classmethod
    def from_url(cls, url: str) -> Optional['KagamizContestSystemService']:
        # example: https://kcs.miz-miz.biz/
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https') and result.netloc == 'kcs.miz-miz.biz':
            return cls()
        return None

    def get_url_of_login_page(self) -> str:
        return 'https://kcs.miz-miz.biz/user/login'

    def is_logged_in(self, *, session: Optional[requests.Session] = None) -> bool:
        session = session or utils.get_default_session()
        url = 'https://kcs.miz-miz.biz/user/login'
        resp = utils.request('GET', url, session=session, allow_redirects=False)
        return resp.status_code == 302


# TODO: add tests for this class
class KagamizContestSystemProblem(onlinejudge.type.Problem):
    """
    :ivar contest_id: :py:class:`int`
    :ivar problem_id: :py:class:`str` like `A` or `%5C`, URL encoded
    """
    def __init__(self, *, contest_id: int, problem_id: str):
        self.contest_id = contest_id
        self.problem_id = problem_id

    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[TestCase]:
        session = session or utils.get_default_session()
        # TODO: implement this function
        logger.error('KagamizContestSystemProblem.download_sample_cases() is not implemented yet')
        return []

    def get_available_languages(self, *, session: Optional[requests.Session] = None) -> List[Language]:
        """
        :raises NotLoggedInError:
        """

        session = session or utils.get_default_session()

        # get
        url = 'https://kcs.miz-miz.biz/contest/{}/submit/{}'.format(self.contest_id, self.problem_id)
        resp = utils.request('GET', url, session=session)

        # parse
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.HTML_PARSER)
        select = soup.find('select', attrs={'name': 'language'})
        if select is None:
            raise NotLoggedInError
        languages = []  # type: List[Language]
        for option in select.findAll('option'):
            languages += [Language(option.attrs['value'], option.string)]
        return languages

    def submit_code(self, code: bytes, language_id: LanguageId, *, filename: Optional[str] = None, session: Optional[requests.Session] = None) -> onlinejudge.type.Submission:
        """
        :raises NotLoggedInError:
        :raises SubmissionError:
        """

        session = session or utils.get_default_session()

        # get
        url = 'https://kcs.miz-miz.biz/contest/{}/submit/{}'.format(self.contest_id, self.problem_id)
        resp = utils.request('GET', url, session=session)

        # parse
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.HTML_PARSER)
        form = soup.find('form', id='submission_data')
        if form is None:
            raise NotLoggedInError
        logger.debug('form: %s', str(form))

        # post
        form = utils.FormSender(form, url=resp.url)
        form.set('language', language_id)
        form.set('code', code)
        try:
            resp = form.request(session=session)
        except requests.exceptions.HTTPError as e:
            raise SubmissionError from e

        # result
        if '/submissions' in resp.url:
            # parse the individual submission page
            submission_url = resp.url
            try:
                url = 'https://kcs.miz-miz.biz/contest/{}/submissions?json=True'.format(self.contest_id)
                resp = utils.request('GET', url, session=session)
                submissions = json.loads(resp.content.decode(resp.encoding))
                submission_id = max([submission['submission_id'] for submission in submissions])
                submission_url = 'https://kcs.miz-miz.biz/contest/{}/code/{}'.format(self.contest_id, submission_id)
            except:
                logger.exception('failed to find the individual submission page. use the list page of all submissions instead.')

            # return the url of the submission page
            logger.info('success: result: %s', submission_url)
            return utils.DummySubmission(submission_url, problem=self)
        else:
            logger.error('failure')
            raise SubmissionError

    def get_url(self) -> str:
        return 'https://kcs.miz-miz.biz/contest/{}/view/{}'.format(self.contest_id, self.problem_id)

    @classmethod
    def from_url(cls, url: str) -> Optional['KagamizContestSystemProblem']:
        result = urllib.parse.urlparse(url)

        # example: https://kcs.miz-miz.biz/contest/2000/view/A
        # example: https://kcs.miz-miz.biz/contest/2000/view/%5C
        if result.scheme in ('', 'http', 'https') \
                and result.netloc == 'kcs.miz-miz.biz':
            parts = utils.normpath(result.path).split('/')
            if len(parts) >= 5 and not parts[0] and parts[1] == 'contest' and parts[3] == 'view':
                problem_id = parts[4]
                if problem_id:
                    try:
                        contest_id = int(parts[2])
                        return cls(contest_id=contest_id, problem_id=problem_id)
                    except ValueError:
                        pass

        return None

    def get_service(self) -> KagamizContestSystemService:
        return KagamizContestSystemService()


onlinejudge.dispatch.services += [KagamizContestSystemService]
onlinejudge.dispatch.problems += [KagamizContestSystemProblem]
