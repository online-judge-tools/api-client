# Python Version: 3.x
import datetime
import http.client
import http.cookiejar
import posixpath
import urllib.parse
from logging import getLogger
from typing import *

import bs4

from onlinejudge.type import *
from onlinejudge.utils import *  # re-export

logger = getLogger(__name__)
HTML_PARSER = 'lxml'


def previous_sibling_tag(tag: bs4.Tag) -> bs4.Tag:
    tag = tag.previous_sibling
    while tag and not isinstance(tag, bs4.Tag):
        tag = tag.previous_sibling
    return tag


def next_sibling_tag(tag: bs4.Tag) -> bs4.Tag:
    tag = tag.next_sibling
    while tag and not isinstance(tag, bs4.Tag):
        tag = tag.next_sibling
    return tag


def get_direct_children_text(tag: bs4.Tag) -> str:
    """get_direct_children_text collects the text which are direct children of the given tag.

    For example, this returns "A - Hello world " for a tag `<h2>A - Hello world <a href="...">Editorial</a></h2>`.
    """

    assert isinstance(tag, bs4.Tag)
    text = ''
    for child in tag.children:
        if isinstance(child, bs4.NavigableString):
            text += child.string
        elif isinstance(child, bs4.Tag) and child.name == 'br':
            text += '\n'
        else:
            pass
    return text


# TODO: Why this returns bs4.NavigableString?
def parse_content(parent: Union[bs4.NavigableString, bs4.Tag, bs4.Comment]) -> bs4.NavigableString:
    """parse_content convert a tag to a string with interpretting `<br>` and ignoring other tags.

    .. seealso::
        https://github.com/kmyk/online-judge-tools/issues/553
    """

    res = ''
    if isinstance(parent, bs4.Comment):
        pass
    elif isinstance(parent, bs4.NavigableString):
        return parent
    else:
        children = parent.contents
        if len(children) == 0:
            html_tag = str(parent)
            return bs4.NavigableString('\n') if 'br' in html_tag else bs4.NavigableString('')
        else:
            for child in children:
                res += parse_content(child)
            if parent.name == 'div':
                res += '\n'

    return bs4.NavigableString(res)


class FormSender:
    def __init__(self, form: bs4.Tag, url: str):
        assert isinstance(form, bs4.Tag)
        assert form.name == 'form'
        self.form = form
        self.url = url
        self.payload = {}  # type: Dict[str, str]
        self.files = {}  # type: Dict[str, bytes]
        for input in self.form.find_all('input'):
            logger.debug('input: %s', str(input))
            if input.attrs.get('type') in ['checkbox', 'radio']:
                continue
            if 'name' in input.attrs and 'value' in input.attrs:
                self.payload[input['name']] = input['value']

    def set(self, key: str, value: str) -> None:
        self.payload[key] = value

    def get(self) -> Dict[str, str]:
        return self.payload

    def set_file(self, key: str, filename: str, content: bytes) -> None:
        self.files[key] = (filename, content)  # type: ignore

    def unset(self, key: str) -> None:
        del self.payload[key]

    def request(self, session: requests.Session, method: Optional[str] = None, action: Optional[str] = None, raise_for_status: bool = True, headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        if method is None:
            method = self.form['method'].upper()
        url = self.url
        if action is None and 'action' in self.form.attrs:
            action = self.form.attrs['action']
        if action is not None:
            url = urllib.parse.urljoin(self.url, action)
        if headers is None:
            headers = {}
        if 'Referer' not in headers:
            headers['Referer'] = self.url
        return request(method, url, session=session, raise_for_status=raise_for_status, data=self.payload, files=self.files, headers=headers, **kwargs)


def dos2unix(s: str) -> str:
    """
    .. deprecated:: 10.1.0
        Use :func:`format_sample_case` instead.
    """

    return s.replace('\r\n', '\n')


def textfile(s: str) -> str:
    """textfile convert a string s to the "text file" defined in POSIX

    .. deprecated:: 10.1.0
        Use :func:`format_sample_case` instead.
    """

    if s.endswith('\n'):
        return s
    elif '\r\n' in s:
        return s + '\r\n'
    else:
        return s + '\n'


def format_sample_case(s: str) -> str:
    """format_sample_case convert a string s to a good form as a sample case.

    A good form means that, it use LR instead of CRLF, it has the trailing newline, and it has no superfluous whitespaces.
    """

    if not s.strip():
        return ''
    lines = s.strip().splitlines()
    lines = [line.strip() + '\n' for line in lines]
    return ''.join(lines)


# We should use this instead of posixpath.normpath
# posixpath.normpath doesn't collapse a leading duplicated slashes. see: https://stackoverflow.com/questions/7816818/why-doesnt-os-normpath-collapse-a-leading-double-slash
def normpath(path: str) -> str:
    path = posixpath.normpath(path)
    if path.startswith('//'):
        path = '/' + path.lstrip('/')
    return path


def request(method: str, url: str, session: requests.Session, raise_for_status: bool = True, **kwargs) -> requests.Response:
    """`request()` is a wrapper of the `requests` package with logging.

    There is a way to bring logs from `requests` via `urllib3`, but we don't use it, because it's not very intended feature ant not very customizable. See https://2.python-requests.org/en/master/api/#api-changes
    """

    assert method in ['GET', 'POST']
    kwargs.setdefault('allow_redirects', True)
    logger.info('network: %s: %s', method, url)
    if 'data' in kwargs:
        logger.debug('network: data: %s', repr(kwargs['data']))  # TODO: prepare a nice filter. This may contain credentials.
    resp = session.request(method, url, **kwargs)
    if resp.url != url:
        logger.info('network: redirected to: %s', resp.url)
    logger.info('network: %s %s', resp.status_code, http.client.responses[resp.status_code])  # e.g. "200 OK" or "503 Service Unavailable"
    if raise_for_status:
        resp.raise_for_status()
    return resp


def remove_prefix(s: str, prefix: str) -> str:
    assert s.startswith(prefix)
    return s[len(prefix):]


def remove_suffix(s: str, suffix: str) -> str:
    assert s.endswith(suffix)
    return s[:-len(suffix)]


tzinfo_jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


class DummySubmission(Submission):
    def __init__(self, url: str, problem: Problem):
        self.url = url
        self.problem = problem

    def download_code(self, session: Optional[requests.Session] = None) -> bytes:
        raise NotImplementedError

    def get_url(self) -> str:
        return self.url

    def download_problem(self, *, session: Optional[requests.Session] = None) -> Problem:
        raise NotImplementedError

    def get_service(self) -> Service:
        raise NotImplementedError

    def __repr__(self) -> str:
        return '{}({}, problem={})'.format(self.__class__, self.url, self.problem)

    @classmethod
    def from_url(cls, s: str) -> Optional[Submission]:
        return None
