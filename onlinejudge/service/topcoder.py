"""
the module for Topcoder (https://topcoder.com/)

.. versionadded:: 10.1.0
"""

import urllib.parse
from logging import getLogger
from typing import *

import bs4
import requests

import onlinejudge._implementation.utils as utils
import onlinejudge.type
from onlinejudge.type import SampleParseError, TestCase

logger = getLogger(__name__)


class TopcoderService(onlinejudge.type.Service):
    def get_url(self) -> str:
        return 'https://arena.topcoder.com/'

    def get_name(self) -> str:
        return 'Topcoder'

    @classmethod
    def from_url(cls, url: str) -> Optional['TopcoderService']:
        # example: https://arena.topcoder.com/
        # example: https://community.topcoder.com/stat?c=problem_statement&pm=10760
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https'):
            if result.netloc in ('topcoder.com', 'arena.topcoder.com', 'community.topcoder.com'):
                return cls()
        return None


# class _TopcoderData(onlinejudge.type.ProblemData):
class _TopcoderData:
    def __init__(self, *, definition: Dict[str, str], raw_sample_cases: List[Tuple[List[str], str]], sample_cases: List[TestCase]):
        self.definition = definition
        self.raw_sample_cases = sample_cases
        self.sample_cases = sample_cases


def _convert_to_greed(x: str) -> str:
    # example: `{1, 0, 1, 1, 0}` -> `5 1 0 1 1 0`
    # example: `"foo"` -> `foo`
    # example: `2` -> `2`
    # example: `{"aa", "bb", "cc"}` -> 3 aa bb cc
    if x.startswith('{') and x.endswith('}'):
        ys = x[1:-1].split(',')
        return ' '.join([str(len(ys)), *map(lambda y: _convert_to_greed(y.strip()), ys)])
    elif x.startswith('"') and x.endswith('"'):
        return x[1:-1]
    else:
        return x


class TopcoderProblem(onlinejudge.type.Problem):
    """
    :ivar problem_id: :py:class:`int`
    """
    def __init__(self, *, problem_id: int):
        self.problem_id = problem_id

    def _download_data(self, *, session: Optional[requests.Session] = None) -> _TopcoderData:
        session = session or utils.get_default_session()

        # download HTML
        url = 'https://community.topcoder.com/stat?c=problem_statement&pm={}'.format(self.problem_id)
        resp = utils.request('GET', url, session=session)

        # parse HTML
        soup = bs4.BeautifulSoup(resp.content.decode(resp.encoding), utils.HTML_PARSER)

        problem_texts = soup.find_all('td', class_='problemText')
        if len(problem_texts) != 1:
            raise SampleParseError("""<td class="problemText"> is not found or not unique""")
        problem_text = problem_texts[0]

        # parse Definition section
        # format:
        #     <tr>...<h3>Definition</h3>...<tr>
        #     <tr><td>...</td>
        #         <td><table>
        #             ...
        #             <tr><td>Class:</td><td>...</td></tr>
        #             <tr><td>Method:</td><td>...</td></tr>
        #             ...
        #         </table></td></tr>
        logger.debug('parse Definition section')
        h3 = problem_text.find('h3', text='Definition')
        if h3 is None:
            raise SampleParseError("""<h3>Definition</h3> is not found""")
        definition = {}
        for text, key in {
                'Class:': 'class',
                'Method:': 'method',
                'Parameters:': 'parameters',
                'Returns:': 'returns',
                'Method signature:': 'method_signature',
        }.items():
            td = h3.parent.parent.next_sibling.find('td', class_='statText', text=text)
            logger.debug('%s', td.parent)
            definition[key] = td.next_sibling.string

        # parse Examples section
        # format:
        #     <tr>...<h3>Examples</h3>...<tr>
        #     <tr><td>0)</td><td></td></tr>
        #     <tr><td></td>
        #         <td><table>
        #             ...
        #             <pre>{5, 8}</pre>
        #             <pre>"foo"</pre>
        #             <pre>3.5</pre>
        #             <pre>Returns: 40.0</pre>
        #             ...
        #         </table></td></tr>
        #     <tr><td>1)</td><td></td></tr>
        #     ...
        logger.debug('parse Examples section')
        h3 = problem_text.find('h3', text='Examples')
        if h3 is None:
            raise SampleParseError("""<h3>Examples</h3> is not found""")

        raw_sample_cases = []  # type: List[Tuple[List[str], str]]
        cursor = h3.parent.parent
        while True:
            # read the header like "0)"
            cursor = cursor.next_sibling
            logger.debug('%s', cursor)
            if not cursor or cursor.name != 'tr':
                break
            if cursor.find('td').string != '{})'.format(len(raw_sample_cases)):
                raise SampleParseError("""<td ...>){})</td> is expected, but not found""".format(len(raw_sample_cases)))

            # collect <pre>s
            cursor = cursor.next_sibling
            logger.debug('%s', cursor)
            if not cursor or cursor.name != 'tr':
                raise SampleParseError("""<tr>...</tr> is expected, but not found""")
            input_items = []
            for pre in cursor.find_all('pre'):
                marker = 'Returns: '
                if pre.string.startswith(marker):
                    output_item = pre.string[len(marker):]
                    break
                else:
                    input_items.append(pre.string)
            else:
                raise SampleParseError("""<pre>Returns: ...</pre> is expected, but not found""")
            raw_sample_cases.append((input_items, output_item))

        # convert samples cases to the Greed format
        sample_cases = []
        for i, (input_items, output_item) in enumerate(raw_sample_cases):
            sample_cases.append(TestCase(
                'example-{}'.format(i),
                'input',
                ('\n'.join(map(_convert_to_greed, input_items)) + '\n').encode(),
                'output',
                (_convert_to_greed(output_item) + '\n').encode(),
            ))

        return _TopcoderData(definition=definition, raw_sample_cases=raw_sample_cases, sample_cases=sample_cases)

    def download_sample_cases(self, *, session: Optional[requests.Session] = None) -> List[TestCase]:
        return self._download_data(session=session).sample_cases

    def get_url(self) -> str:
        return 'https://community.topcoder.com/stat?c=problem_statement&pm={}'.format(self.problem_id)

    @classmethod
    def from_url(cls, url: str) -> Optional['TopcoderProblem']:
        # example: https://arena.topcoder.com/index.html#/u/practiceCode/14230/10838/10760/1/303803
        # example: https://community.topcoder.com/stat?c=problem_statement&pm=10760
        result = urllib.parse.urlparse(url)
        if result.scheme in ('', 'http', 'https'):
            if result.netloc == 'arena.topcoder.com' and utils.normpath(result.path) in ('/', '/index.html'):
                dirs = utils.normpath(result.fragment).split('/')
                if len(dirs) == 8 and dirs[0] == '' and dirs[1] == 'u' and dirs[2] == 'practiceCode':
                    try:
                        _ = int(dirs[3])  # round_id
                        _ = int(dirs[4])  # component_id
                        problem_id = int(dirs[5])
                        _ = int(dirs[6])  # division_id
                        _ = int(dirs[7])  # room_id
                    except ValueError:
                        pass
                    else:
                        return cls(problem_id=problem_id)
            if result.netloc == 'community.topcoder.com' and utils.normpath(result.path) == '/stat':
                query = urllib.parse.parse_qs(result.query)
                if query.get('c') == ['problem_statement'] and len(query.get('pm', [])) == 1:
                    try:
                        problem_id = int(query['pm'][0])
                    except ValueError:
                        pass
                    else:
                        return cls(problem_id=problem_id)
        return None

    def get_service(self) -> TopcoderService:
        return TopcoderService()


onlinejudge.dispatch.services += [TopcoderService]
onlinejudge.dispatch.problems += [TopcoderProblem]
