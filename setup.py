#!/usr/bin/env python3
import importlib
import importlib.util

from setuptools import find_packages, setup


def load_module(name, location):
    spec = importlib.util.spec_from_file_location(name, location)
    version = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version)
    return version


about = load_module('onlinejudge.__about__', 'onlinejudge/__about__.py')

setup(
    name=about.__package_name__,
    version=about.__version__,
    author=about.__author__,
    author_email=about.__email__,
    url=about.__url__,
    license=about.__license__,
    description=about.__description__,
    python_requires='>=3.6',
    install_requires=[
        'appdirs >= 1',
        'beautifulsoup4 >= 4',
        'colorlog >= 4.1.0',
        'lxml >= 4',
        'requests >= 2',
        'toml >= 0.10',
        'jsonschema >= 3.2',
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={
        "onlinejudge": ["py.typed"],
        "onlinejudge_workaround_for_conflict": ["py.typed"],
    },
    entry_points={
        'console_scripts': [
            'oj-api = onlinejudge_api.main:main',
        ],
    },
)
