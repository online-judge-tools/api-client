import pathlib
from logging import getLogger
from typing import *

import requests

import onlinejudge._implementation.language_guessing as language_guessing
from onlinejudge.type import *

logger = getLogger()

schema_example = {
    "id": "61",
    "description": "GNU G++17 9.2.0 (64 bit, msys 2)",
    "context": {
        "problem": {
            "url": "http://codeforces.com/contest/1373/problem/A",
        },
    },
}  # type: Dict[str, Any]

schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
        },
        "description": {
            "type": "string",
        },
        "context": {
            "type": "object",
            "properties": {
                "problem": {
                    "context": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "format": "url",
                            },
                        },
                    },
                },
            },
        },
    },
    "required": ["id", "description"],
}  # type: Dict[str, Any]


def main(problem: Problem, *, path: pathlib.Path, session: requests.Session) -> Dict[str, Any]:
    """
    :raises Exception:
    """

    with open(str(path), "rb") as fh:
        code = fh.read()
    try:
        available_languages = problem.get_available_languages(session=session)
    except Exception as e:
        logger.error("failed to list available languages: %s", e)
        raise e

    # This uses the recommended settings becuase this is a command expected to work without customizing. If more customization is needed, users (i.e. developers) should write code by themselves for their tools.
    guessed_languages = language_guessing.guess_languages_of_file(
        path,
        code,
        languages=available_languages,
        cxx_latest=True,
        cxx_compiler='gcc',
        python_version='auto',
        python_interpreter='cpython',
    )
    if len(guessed_languages) == 0:
        raise RuntimeError('no language id found')
    elif len(guessed_languages) == 1:
        guessed_language = guessed_languages[0]
    else:
        raise RuntimeError('too many language ids are found')

    result = {
        "id": guessed_language.id,
        "description": guessed_language.name,
        "context": {
            "problem": {
                "url": problem.get_url(),
            },
        },
    }  # type: Dict[str, Any]
    return result
