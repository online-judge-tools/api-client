#!/usr/bin/env python3
import argparse
import os
import pathlib


def main():
    parser = argparse.ArgumentParser(description='Categorize and list test files in the tests/ directory')
    parser.add_argument('keyword', choices=('stable', 'unstable'))
    args = parser.parse_args()

    tests = pathlib.Path('tests')
    unstable = [
        tests / 'get_problem_codeforces.py',
        tests / 'get_contest_codeforces.py',
        tests / 'get_problem_poj.py',
        tests / 'get_problem_topcoder.py',
        tests / 'service_codeforces.py',
        tests / 'service_codechef.py',
    ]

    if args.keyword == 'unstable':
        files = unstable
    elif args.keyword == 'stable':
        files = [file for file in tests.glob('*.py') if file not in unstable]
    else:
        assert False

    GITHUB_OUTPUT = 'GITHUB_OUTPUT'  # pylint: disable=invalid-name
    if GITHUB_OUTPUT in os.environ:
        with open(os.environ[GITHUB_OUTPUT], 'a', encoding='utf-8') as f:
            print('files=', *map(str, files), file=f)


if __name__ == '__main__':
    main()
