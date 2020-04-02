import argparse
import json
import pathlib
import sys
import textwrap
import traceback
from logging import getLogger
from typing import *

import jsonschema
import onlinejudge_api.get_contest as get_contest
import onlinejudge_api.get_problem as get_problem
import onlinejudge_api.login_service as login_service
import onlinejudge_api.submit_code as submit_code

import onlinejudge
import onlinejudge._implementation.utils as utils
from onlinejudge.service.yukicoder import YukicoderProblem, YukicoderService
from onlinejudge.type import *

logger = getLogger()


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Tools for online judge services')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-c', '--cookie', type=pathlib.Path, default=utils.default_cookie_path, help='path to cookie. (default: {})'.format(utils.default_cookie_path))
    parser.add_argument('--yukicoder-token', type=str)
    subparsers = parser.add_subparsers(dest='subcommand', help='for details, see "{} COMMAND --help"'.format(sys.argv[0]))

    # get-problem
    epilog = textwrap.dedent("""\
        supported services:
          Anarchy Golf
          Aizu Online Judge (including the Arena)
          AtCoder
          Codeforces
          yukicoder
          CS Academy
          HackerRank
          PKU JudgeOnline
          Kattis
          Toph (Problem Archive)
          CodeChef
          Facebook Hacker Cup
          Library Checker (https://judge.yosupo.jp/)

        supported services with --system:
          Aizu Online Judge
          yukicoder
          Library Checker (https://judge.yosupo.jp/)

        JSON schema:
        {}

        JSON sample:
        {}
        """).format(
        textwrap.indent(json.dumps(get_problem.schema, indent=2), '  '),
        textwrap.indent(json.dumps(get_problem.schema_example, indent=2), '  '),
    )
    jsonschema.validate(get_problem.schema_example, get_problem.schema)

    subparser = subparsers.add_parser('get-problem', formatter_class=argparse.RawTextHelpFormatter, epilog=epilog)
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

        JSON schema:
        {}

        JSON example:
        {}
        ''').format(
        textwrap.indent(json.dumps(get_contest.schema, indent=2), '  '),
        textwrap.indent(json.dumps(get_contest.schema_example, indent=2), '  '),
    )
    jsonschema.validate(get_contest.schema_example, get_contest.schema)

    subparser = subparsers.add_parser('get-contest', formatter_class=argparse.RawTextHelpFormatter, epilog=epilog)
    subparser.add_argument('url')
    subparser.add_argument('--full', action='store_true')

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
    subparser.add_argument('--username')
    subparser.add_argument('--password')
    subparser.add_argument('--check', action='store_true', help='check whether you are logged in or not')

    # submit-code
    epilog = textwrap.dedent('''\
        supported services:
          AtCoder
          Codeforces
          yukicoder
          HackerRank
          Toph (Problem Archive)

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
    subparser.add_argument('file', type=pathlib.Path)
    subparser.add_argument('url', help='the URL of the problem to submit. if not given, guessed from history of download command.')
    subparser.add_argument('--language', required=True, type=LanguageId, help='''a language ID; you can get the values from "availableLanguages" field of "get-problem" subcommand with "--full" option''')

    # spawn-server
    subparser = subparsers.add_parser('spawn-server')

    return parser


def run(args: Optional[List[str]] = None) -> None:
    parser = get_parser()
    parsed = parser.parse_args(args=args)

    problem = onlinejudge.dispatch.problem_from_url(getattr(parsed, 'url', ''))
    contest = onlinejudge.dispatch.contest_from_url(getattr(parsed, 'url', ''))
    service = onlinejudge.dispatch.service_from_url(getattr(parsed, 'url', ''))

    try:
        with utils.with_cookiejar(utils.new_session_with_our_user_agent(), path=parsed.cookie) as session:
            is_yukicoder = isinstance(problem, YukicoderProblem) or isinstance(service, YukicoderService)
            if parsed.yukicoder_token and is_yukicoder:
                session.headers['Authorization'] = 'Bearer {}'.format(parsed.yukicoder_token)

            result = None  # type: Optional[Dict[str, Any]]
            schema = {}  # type: Dict[str, Any]
            if parsed.subcommand == 'get-problem':
                if problem is None:
                    parser.error("unsupported URL: {}".format(repr(parsed.url)))
                result = get_problem.main(problem, is_system=parsed.system, is_full=parsed.full, is_compatibility=parsed.compatibility, session=session)
                if parsed.compatibility:
                    schema = get_problem.schema_compatibility
                else:
                    schema = get_problem.schema

            elif parsed.subcommand == 'get-contest':
                if contest is None:
                    parser.error("unsupported URL: {}".format(repr(parsed.url)))
                result = get_contest.main(contest, is_full=parsed.full, session=session)
                schema = get_contest.schema

            elif parsed.subcommand == 'login-service':
                if service is None:
                    parser.error("unsupported URL: {}".format(repr(parsed.url)))
                result = login_service.main(service, username=parsed.username, password=parsed.password, check_only=parsed.check, session=session)
                schema = login_service.schema

            elif parsed.subcommand == 'submit-code':
                if problem is None:
                    parser.error("unsupported URL: {}".format(repr(parsed.url)))
                result = submit_code.main(problem, file=parsed.file, language_id=parsed.language, session=session)
                schema = submit_code.schema

            elif parsed.subcommand is None:
                parser.print_help()
                result = None

            else:
                assert False

    except:
        etype, evalue, _ = sys.exc_info()
        print(json.dumps({
            "status": "error",
            "messages": [*map(lambda line: line.strip(), traceback.format_exception_only(etype, evalue))],
            "result": None,
        }))
        raise

    else:
        if result is not None:
            print(json.dumps({
                "status": "ok",
                "messages": [],
                "result": result,
            }))

            try:
                jsonschema.validate(result, schema)
            except jsonschema.exceptions.ValidationError:
                logger.exception('validation failure')


def main() -> None:
    try:
        run()
    except SystemExit:
        raise
    except:
        logger.exception('something wrong')
        sys.exit(1)


if __name__ == '__main__':
    main()
