"""
isort: skip_file
"""

# This is a workaround for the issue https://github.com/online-judge-tools/oj/issues/755
# pylint: disable=unused-import,ungrouped-imports
try:
    import onlinejudge.service
except ImportError as e:
    import json
    print(json.dumps({
        "status": "error",
        "messages": ["Due to a known bug, the online-judge-tools is not yet properly installed. Please re-run $ pip3 install --force-reinstall online-judge-api-client"],
        "result": None,
    }))
    raise SystemExit(1) from e
# pylint: enable=unused-import,ungrouped-imports

import argparse
import json
import os
import pathlib
import sys
import textwrap
import time
import traceback
from logging import DEBUG, INFO, basicConfig, getLogger
from typing import *

import jsonschema
import onlinejudge_api.get_contest as get_contest
import onlinejudge_api.get_problem as get_problem
import onlinejudge_api.get_service as get_service
import onlinejudge_api.guess_language_id as guess_language_id
import onlinejudge_api.login_service as login_service
import onlinejudge_api.submit_code as submit_code
import requests

import onlinejudge._implementation.utils as utils
import onlinejudge.dispatch as dispatch
from onlinejudge.__about__ import __package_name__, __version__
from onlinejudge.service.atcoder import AtCoderProblem
from onlinejudge.service.yukicoder import YukicoderProblem, YukicoderService
from onlinejudge.type import *

logger = getLogger(__name__)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Tools for online judge services')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--cookie', type=pathlib.Path, default=utils.default_cookie_path, help='specify the path to the cookie.jar. (default: {})'.format(utils.default_cookie_path))
    parser.add_argument('--wait', type=float, default=1.0, help='specify the duration to sleep to prevent impolite scraping. Please set --wait=0.0 after understanding why this option exists.  (default: 1.0)')
    parser.add_argument('--user-agent', help="specify the User Agent. We recommend you set this because some websites ban the default User Agent of Python's requests library.  (default: {})".format(requests.utils.default_user_agent()))
    parser.add_argument('--yukicoder-token', help='specify the token of yukicoder. This option is a dummy. For a security reason, use the $YUKICODER_TOKEN envvar.  (default: $YUKICODER_TOKEN)')
    subparsers = parser.add_subparsers(dest='subcommand', help='for details, see "{} COMMAND --help"'.format(sys.argv[0]))

    # get-problem
    epilog = textwrap.dedent("""\
        supported services:
          Aizu Online Judge
          Anarchy Golf
          AtCoder
          CodeChef
          Codeforces
          CS Academy
          Facebook Hacker Cup
          Google Code Jam
          Google KickStart
          HackerRank
          Kattis
          Library Checker
          PKU JudgeOnline
          Toph
          yukicoder

        supported services with --system:
          Aizu Online Judge
          AtCoder
          HackerRank
          Library Checker
          yukicoder

        JSON schema:
        {}

        JSON sample:
        {}
        """).format(
        textwrap.indent(json.dumps(get_problem.schema, indent=2), '  '),
        textwrap.indent(json.dumps(get_problem.schema_example, indent=2), '  '),
    )
    jsonschema.validate(get_problem.schema_example, get_problem.schema)

    subparser = subparsers.add_parser('get-problem', help='get information about a problem', formatter_class=argparse.RawTextHelpFormatter, epilog=epilog)
    subparser.add_argument('url')
    subparser.add_argument('--system', action='store_true', help='download system testcases')
    group = subparser.add_mutually_exclusive_group()
    group.add_argument('--full', action='store_true')
    group.add_argument('--compatibility', action='store_true', help='add and fix some fields for compatibility to competitive-companion')

    # get-contest
    epilog = textwrap.dedent('''\
        supported services:
          AtCoder
          Codeforces
          yukicoder

        JSON schema:
        {}

        JSON example:
        {}
        ''').format(
        textwrap.indent(json.dumps(get_contest.schema, indent=2), '  '),
        textwrap.indent(json.dumps(get_contest.schema_example, indent=2), '  '),
    )
    jsonschema.validate(get_contest.schema_example, get_contest.schema)

    subparser = subparsers.add_parser('get-contest', help='get information about a contest', formatter_class=argparse.RawTextHelpFormatter, epilog=epilog)
    subparser.add_argument('url')
    subparser.add_argument('--full', action='store_true')

    # get-service
    epilog = textwrap.dedent('''\
        supported services:
          all services

        JSON schema:
        {}

        JSON example:
        {}
        ''').format(
        textwrap.indent(json.dumps(get_service.schema, indent=2), '  '),
        textwrap.indent(json.dumps(get_service.schema_example, indent=2), '  '),
    )
    jsonschema.validate(get_service.schema_example, get_service.schema)

    subparser = subparsers.add_parser('get-service', help='get information about a service', formatter_class=argparse.RawTextHelpFormatter, epilog=epilog)
    subparser.add_argument('url')
    subparser.add_argument('--list-contests', action='store_true')

    # login-service
    epilog = textwrap.dedent('''\
        supported services (password):
          AtCoder
          Codeforces

        JSON schema:
        {}

        JSON example:
        {}
        ''').format(
        textwrap.indent(json.dumps(login_service.schema, indent=2), '  '),
        textwrap.indent(json.dumps(login_service.schema_example, indent=2), '  '),
    )
    jsonschema.validate(login_service.schema_example, login_service.schema)

    subparser = subparsers.add_parser('login-service', help='login to a service', formatter_class=argparse.RawTextHelpFormatter, epilog=epilog)
    subparser.add_argument('url')
    subparser.add_argument('--username', default=os.environ.get('USERNAME'), help='specify the username.  (default: $USERNAME)')
    subparser.add_argument('--password', help="specify the password. This option is a dummy. For a security reason, use the $PASSWORD envvar.  (default: $PASSWORD)")
    subparser.add_argument('--check', action='store_true', help='check whether you are logged in or not')

    # submit-code
    epilog = textwrap.dedent('''\
        supported services:
          AtCoder
          Codeforces
          HackerRank
          Kagamiz Contest System
          Toph
          yukicoder

        JSON schema:
        {}

        JSON example:
        {}
        ''').format(
        textwrap.indent(json.dumps(submit_code.schema, indent=2), '  '),
        textwrap.indent(json.dumps(submit_code.schema_example, indent=2), '  '),
    )
    jsonschema.validate(submit_code.schema_example, submit_code.schema)

    subparser = subparsers.add_parser('submit-code', help='submit your solution', formatter_class=argparse.RawTextHelpFormatter, epilog=epilog)
    subparser.add_argument('url', help='the URL of the problem to submit')
    subparser.add_argument('--file', required=True, type=pathlib.Path)
    subparser.add_argument('--language', required=True, type=LanguageId, help='''a language ID; you can get the values from "availableLanguages" field of "get-problem" subcommand with "--full" option''')

    # guess-language-id
    epilog = textwrap.dedent('''\
        JSON schema:
        {}

        JSON example:
        {}
        ''').format(
        textwrap.indent(json.dumps(guess_language_id.schema, indent=2), '  '),
        textwrap.indent(json.dumps(guess_language_id.schema_example, indent=2), '  '),
    )
    jsonschema.validate(guess_language_id.schema_example, guess_language_id.schema)

    subparser = subparsers.add_parser('guess-language-id', help='guess the language id for your solution', formatter_class=argparse.RawTextHelpFormatter, epilog=epilog)
    subparser.add_argument('url', help='the URL of the problem to submit')
    subparser.add_argument('--file', required=True, type=pathlib.Path)

    return parser


def main(args: Optional[List[str]] = None, *, debug: bool = False) -> Dict[str, Any]:
    parser = get_parser()
    parsed = parser.parse_args(args=args)

    # configure logging
    level = INFO
    if parsed.verbose:
        level = DEBUG
    basicConfig(level=level)

    # print the version to help to support users
    logger.info('%s %s', __package_name__, __version__)

    # do sleep to prevent impolite scraping
    logger.info('sleep %f sec', parsed.wait)
    time.sleep(parsed.wait)

    # parse the URL
    problem = dispatch.problem_from_url(getattr(parsed, 'url', ''))
    contest = dispatch.contest_from_url(getattr(parsed, 'url', ''))
    service = dispatch.service_from_url(getattr(parsed, 'url', ''))

    # prepare a session
    session = requests.Session()
    session.headers['User-Agent'] = parsed.user_agent

    # set yukicoder's token
    YUKICODER_TOKEN = 'YUKICODER_TOKEN'  # pylint: disable=invalid-name
    if parsed.yukicoder_token is not None:
        parser.error("don't use --yukicoder-token. use $YUKICODER_TOKEN")
    if YUKICODER_TOKEN in os.environ:
        parsed.yukicoder_token = os.environ[YUKICODER_TOKEN]
        if not debug:
            del os.environ[YUKICODER_TOKEN]
    is_yukicoder = isinstance(problem, YukicoderProblem) or isinstance(service, YukicoderService)
    if parsed.yukicoder_token and is_yukicoder:
        session.headers['Authorization'] = 'Bearer {}'.format(parsed.yukicoder_token)

    # set Dropbox's token
    DROPBOX_TOKEN = 'DROPBOX_TOKEN'  # pylint: disable=invalid-name
    dropbox_token: Optional[str] = None
    if DROPBOX_TOKEN in os.environ:
        dropbox_token = os.environ[DROPBOX_TOKEN]
        if not debug:
            del os.environ[DROPBOX_TOKEN]
    is_atcoder = isinstance(problem, AtCoderProblem)
    if dropbox_token and is_atcoder and parsed.system:
        session.headers['Authorization'] = 'Bearer {}'.format(dropbox_token)

    # set password to login from the environment variable
    if parsed.subcommand == 'login-service':
        if parsed.password is not None:
            parser.error("don't use --password. use $PASSWORD")
        parsed.password = os.environ.get('PASSWORD')
        if not debug:
            del os.environ['PASSWORD']

    try:
        with utils.with_cookiejar(session, path=parsed.cookie) as session:
            result = None  # type: Optional[Dict[str, Any]]
            schema = {}  # type: Dict[str, Any]

            if parsed.subcommand == 'get-problem':
                if problem is None:
                    raise ValueError("unsupported URL: {}".format(repr(parsed.url)))
                result = get_problem.main(problem, is_system=parsed.system, is_full=parsed.full, is_compatibility=parsed.compatibility, session=session)
                if parsed.compatibility:
                    schema = get_problem.schema_compatibility
                else:
                    schema = get_problem.schema

            elif parsed.subcommand == 'get-contest':
                if contest is None:
                    raise ValueError("unsupported URL: {}".format(repr(parsed.url)))
                result = get_contest.main(contest, is_full=parsed.full, session=session)
                schema = get_contest.schema

            elif parsed.subcommand == 'get-service':
                if service is None:
                    raise ValueError("unsupported URL: {}".format(repr(parsed.url)))
                result = get_service.main(service, does_list_contests=parsed.list_contests, session=session)
                schema = get_service.schema

            elif parsed.subcommand == 'login-service':
                if service is None:
                    raise ValueError("unsupported URL: {}".format(repr(parsed.url)))
                result = login_service.main(service, username=parsed.username, password=parsed.password, check_only=parsed.check, session=session)
                schema = login_service.schema

            elif parsed.subcommand == 'submit-code':
                if problem is None:
                    raise ValueError("unsupported URL: {}".format(repr(parsed.url)))
                result = submit_code.main(problem, file=parsed.file, language_id=parsed.language, session=session)
                schema = submit_code.schema

            elif parsed.subcommand == 'guess-language-id':
                if problem is None:
                    raise ValueError("unsupported URL: {}".format(repr(parsed.url)))
                result = guess_language_id.main(problem, path=parsed.file, session=session)
                schema = guess_language_id.schema

            elif parsed.subcommand is None:
                parser.print_help()
                result = None

            else:
                assert False

    except Exception as e:
        etype, evalue, _ = sys.exc_info()
        logger.exception('%s', evalue)
        wrapped = {
            "status": "error",
            "messages": [*map(lambda line: line.strip(), traceback.format_exception_only(etype, evalue))],
            "result": None,
        }  # type: Dict[str, Any]
        if debug:
            return wrapped
        else:
            print(json.dumps(wrapped))
            raise SystemExit(1) from e

    else:
        if result is None:
            # no subcommand given
            if debug:
                return {
                    "status": "ok",
                    "messages": [],
                    "result": None,
                }
            else:
                raise SystemExit(0)

        wrapped = {
            "status": "ok",
            "messages": [],
            "result": result,
        }
        if not debug:
            print(json.dumps(wrapped))

        try:
            jsonschema.validate(result, schema)
        except jsonschema.exceptions.ValidationError as e:
            logger.debug('%s', e)

        if debug:
            return wrapped
        else:
            raise SystemExit(0)


if __name__ == '__main__':
    main()
