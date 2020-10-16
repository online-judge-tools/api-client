"""
the module for LeetCode (https://leetcode.com/)
"""

import time
import urllib.parse
from logging import getLogger
from typing import *

import bs4
import requests

import onlinejudge._implementation.utils as utils
import onlinejudge.type
from onlinejudge.type import *

logger = getLogger(__name__)


class LeetCodeService(onlinejudge.type.Service):
    def get_url(self) -> str:
        return 'https://leetcode.com/'

    def get_name(self) -> str:
        return 'LeetCode'

    def _set_request_header(self, session: Optional[requests.Session] = None) -> requests.Session:
        session = session or utils.get_default_session()

        service_url = self.get_url()
        session.headers.update({
            'Origin': service_url,
            'Referer': service_url,
            'Content-type': 'application/json',
        })

        # get csrf token from cookies and set it to header as well
        for cookie in session.cookies:
            if cookie.domain == 'leetcode.com' and cookie.name == 'csrftoken':
                if cookie.value is not None:
                    session.headers.update({
                        'X-CSRFToken': cookie.value,
                    })
                break

        return session

    @classmethod
    def from_url(cls, url: str) -> Optional['LeetCodeService']:
        # example: https://leetcode.com/
        result = urllib.parse.urlparse(url)
        if result.scheme not in ('', 'http', 'https'):
            return None
        if result.netloc != 'leetcode.com':
            return None
        return cls()

    def is_logged_in(self, *, session: Optional[requests.Session] = None) -> bool:
        session = self._set_request_header(session)
        json_body = {
            'operationName': 'globalData',
            'query': '\n'.join([
                'query globalData {',
                '    userStatus {',
                '        isSignedIn',
                '    }',
                '}',
            ]),
        }
        resp = utils.request('POST', 'https://leetcode.com/graphql', session=session, json=json_body)
        json_resp = resp.json()
        return json_resp['data']['userStatus']['isSignedIn']


class LeetCodeProblem(onlinejudge.type.Problem):
    """
    :ivar title_slug: :py:class:`str`
    """
    def __init__(self, *, title_slug: str):
        self.title_slug = title_slug

    def _set_request_header(self, session: Optional[requests.Session] = None) -> requests.Session:
        service = self.get_service()
        session = service._set_request_header(session)
        service_url = service.get_url()
        session.headers.update({
            'Referer': f'{service_url}problems/{self.title_slug}/',
        })
        return session

    # TODO: enable to get premium only questions as well
    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[TestCase]:
        session = self._set_request_header(session)
        json_body = {
            'operationName': 'getQuestionDetail',
            'query': '\n'.join([
                'query getQuestionDetail($titleSlug: String!) {',
                '    question(titleSlug: $titleSlug) {',
                '        content',
                '    }',
                '}',
            ]),
            'variables': {
                'titleSlug': self.title_slug
            },
        }

        resp = utils.request('POST', 'https://leetcode.com/graphql', session=session, json=json_body)
        json_resp = resp.json()
        content_html = json_resp['data']['question']['content']
        if content_html is None:
            logger.warning("This problem seems to be locked: need premium?")
            return []
        soup = bs4.BeautifulSoup(content_html, utils.html_parser)
        test_cases = []

        for num, pre in enumerate(soup.find_all('pre')):
            children = pre.contents
            idx, input_data, output_data = 0, '', ''

            # find input data
            while (idx < len(children) and (children[idx].name != 'strong' or len(children[idx].contents) != 1 or 'input' not in children[idx].contents[0].lower())):
                idx += 1
            idx += 1
            if idx < len(children):
                input_data = children[idx].strip()

            # find output data
            while (idx < len(children) and (children[idx].name != 'strong' or len(children[idx].contents) != 1 or 'output' not in children[idx].contents[0].lower())):
                idx += 1
            idx += 1
            if idx < len(children):
                output_data = children[idx].strip()

            if input_data and output_data:
                test_cases.append(TestCase(
                    f'Example {num + 1}',
                    'Input',
                    input_data.encode(),
                    'Output',
                    output_data.encode(),
                ))
        return test_cases

    def get_available_languages(self, *, session: Optional[requests.Session] = None) -> List[Language]:
        session = self._set_request_header(session)
        json_body = {
            'operationName': 'getQuestionDetail',
            'query': '\n'.join([
                'query getQuestionDetail($titleSlug: String!) {',
                '    question(titleSlug: $titleSlug) {',
                '        codeSnippets {',
                '            lang',
                '            langSlug',
                '        }',
                '    }',
                '}',
            ]),
            'variables': {
                'titleSlug': self.title_slug
            },
        }

        resp = utils.request('POST', 'https://leetcode.com/graphql', session=session, json=json_body)
        json_resp = resp.json()
        code_snippets = json_resp['data']['question']['codeSnippets']
        languages = []  # type: List[Language]
        for code_definition in code_snippets:
            languages.append(Language(code_definition['langSlug'], code_definition['lang']))
        return languages

    def submit_code(self, code: bytes, language_id: LanguageId, *, filename: Optional[str] = None, session: Optional[requests.Session] = None) -> onlinejudge.type.Submission:
        """
        :raises NotLoggedInError:
        :raises SubmissionError:
        """

        if not self.get_service().is_logged_in(session=session):
            logger.error('not logged in or session expired')
            raise NotLoggedInError

        session = self._set_request_header(session)

        # get questionId
        json_body = {
            'operationName': 'getQuestionDetail',
            'query': '\n'.join([
                'query getQuestionDetail($titleSlug: String!) {',
                '    question(titleSlug: $titleSlug) {',
                '        questionId',
                '    }',
                '}',
            ]),
            'variables': {
                'titleSlug': self.title_slug
            },
        }
        resp = utils.request('POST', 'https://leetcode.com/graphql', session=session, json=json_body)
        json_resp = resp.json()
        questionId = json_resp['data']['question']['questionId']

        # submit code
        json_body = {
            'lang': language_id,
            'question_id': questionId,
            'typed_code': code.decode(),
        }
        retry_count = 5
        while True:
            try:
                resp = utils.request('POST', f'https://leetcode.com/problems/{self.title_slug}/submit/', session=session, json=json_body)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code != 429:
                    raise SubmissionError from e
                elif retry_count == 0:
                    logger.error('Failed 5 times to sumit your code: abort')
                    raise SubmissionError from e
                else:
                    retry_count -= 1
                    logger.warning('LeetCode\'s submission rate limit exceeded: try in 3 seconds')
                    time.sleep(3)
                    continue
            break
        json_resp = resp.json()
        submission_id = json_resp['submission_id']

        # polling to the result
        while True:
            resp = utils.request('GET', f'https://leetcode.com/submissions/detail/{submission_id}/check/', session=session)
            json_resp = resp.json()
            if json_resp['state'] == 'SUCCESS':
                break
            logger.warning('Waiting for the result of your submission(id: %s)', submission_id)
            time.sleep(1 / 3)

        result_url = f'https://leetcode.com/submissions/detail/{submission_id}/'
        logger.info('success: result: %s', result_url)
        return utils.DummySubmission(result_url, problem=self)

    def get_url(self) -> str:
        return f'https://leetcode.com/problems/{self.title_slug}/'

    @classmethod
    def from_url(cls, url: str) -> Optional['LeetCodeProblem']:
        # example: https://leetcode.com/problems/two-sum/
        result = urllib.parse.urlparse(url)
        if result.scheme not in ('', 'http', 'https'):
            return None
        if result.netloc != 'leetcode.com':
            return None
        parts = utils.normpath(result.path).split('/')[1:]
        if len(parts) < 2 or parts[0] != 'problems':
            return None
        return cls(title_slug=parts[1])

    def get_service(self) -> LeetCodeService:
        return LeetCodeService()


onlinejudge.dispatch.services += [LeetCodeService]
onlinejudge.dispatch.problems += [LeetCodeProblem]
