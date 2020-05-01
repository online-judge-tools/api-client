#!/usr/bin/env python3
import argparse
import pathlib


def main():
    parser = argparse.ArgumentParser(description='Categorize and list test files in the tests/ directory')
    parser.add_argument('keyword', choices=('stable', 'unstable'))
    args = parser.parse_args()

    tests = pathlib.Path('tests')
    unstable = [
        tests / 'service_codeforces.py',
        tests / 'service_codechef.py',
        tests / 'service_poj.py',
    ]

    if args.keyword == 'unstable':
        files = unstable
    elif args.keyword == 'stable':
        files = [file for file in tests.glob('*.py') if file not in unstable]
    else:
        assert False

    print('::set-output name=files::', *map(str, files))


if __name__ == '__main__':
    main()
