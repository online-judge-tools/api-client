#!/usr/bin/env python3
import imp

from setuptools import find_packages, setup


def load_module(module_path):
    path = None
    for name in module_path.split('.'):
        file, path, description = imp.find_module(name, path)
        path = [path]
    return imp.load_module(name, file, path[0], description)


version = load_module('onlinejudge.__about__')

setup(
    name='online-judge-api-client',
    version='9.2.0',
    author='Kimiyuki Onaka',
    author_email='kimiyuki95@gmail.com',
    url='https://github.com/kmyk/online-judge-api-client',
    license='MIT License',
    description='command and library to develop tools for competitive programming',
    python_requires='>=3.5',
    install_requires=[
        'appdirs >= 1',
        'beautifulsoup4 >= 4',
        'colorama >= 0.3',
        'lxml >= 4',
        'requests >= 2',
        'toml >= 0.10',
        'jsonschema >= 3.2',
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'oj-api = onlinejudge_api.main:main',
        ],
    },
)
