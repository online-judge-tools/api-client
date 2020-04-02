from logging import getLogger
from typing import *

from onlinejudge.service.atcoder import AtCoderProblem
from onlinejudge.service.codeforces import CodeforcesProblem
from onlinejudge.type import *

logger = getLogger()
schema_example: Dict[str, Any] = {
    "url": "https://atcoder.jp/contests/abc160/tasks/abc160_c",
    "name": "Traveling Salesman around Lake",
    "context": {
        "contest": {
            "name": "AtCoder Beginner Contest 160",
            "url": "https://atcoder.jp/contests/abc160",
        },
        "alphabet": "C",
    },
    "memoryLimit": 1024,
    "timeLimit": 2000,
    "tests": [
        {
            "input": "20 3\n5 10 15\n",
            "output": "10\n",
        },
        {
            "input": "20 3\n0 5 15\n",
            "output": "10\n",
        },
    ],
}

schema: Dict[str, Any] = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
            "format": "uri",
        },
        "name": {
            "type": "string",
            "description": """the title of the problem without alphabets, i.e. "Xor Sum" is used instead of "D - Xor Sum"; because in many contest sites, the alphabets are attributes belonging to the relation between problems and contests, rather than only the problem""",
            "examples": ["Xor Sum", "K-th Beautiful String"],
        },
        "context": {
            "type": "object",
            "properties": {
                "contest": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "format": "uri",
                        },
                        "name": {
                            "type": "string",
                        },
                    },
                },
                "alphabet": {
                    "type": "string",
                },
            },
        },
        "memoryLimit": {
            "type": "integer",
            "description": "in megabytes (MB); not in mebibytes (MiB)",
        },
        "timeLimit": {
            "type": "integer",
            "description": "in milliseconds (msec)",
        },
        "tests": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                    "input": {
                        "type": "string",
                    },
                    "output": {
                        "type": "string",
                    },
                },
                "required": ["input", "output"],
            },
            "examples": [
                [
                    {
                        "input": "35\n",
                        "output": "57\n",
                    },
                    {
                        "input": "57\n",
                        "output": "319\n",
                    },
                ],
            ],
        },
        "availableLanguages": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "examples": ["3000", "3001", "cpp", "C++"],
                    },
                    "description": {
                        "type": "string",
                        "examples": ["C++14 (GCC 5.4.1)", "Python 3 (3.4.3)"],
                    },
                },
                "required": ["id", "description"],
            },
        },
        "raw": {
            "type": "object",
            "properties": {
                "html": {
                    "type": "string",
                    "contentMediaType": "text/html",
                },
                "json": {
                    "type": "string",
                    "contentMediaType": "application/json",
                },
            },
        },
    },
    "required": [
        "url",
        "tests",
        "context",
    ],
}

schema_compatibility: Dict[str, Any] = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "group": {
            "type": "string",
        },
        "url": {
            "type": "string",
            "format": "uri",
        },
        "interactive": {
            "type": "boolean",
        },
        "memoryLimit": {
            "type": "integer",
        },
        "timeLimit": {
            "type": "integer",
        },
        "testType": {
            "type": "string",
            "enum": ["single", "multiNumber"],
        },
        "input": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["stdin", "file"],
                },
                "fileName": {
                    "type": "string",
                },
            },
            "required": ["type"],
            "additionalProperties": False,
        },
        "output": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["stdout", "file"],
                },
                "fileName": {
                    "type": "string",
                },
            },
            "required": ["type"],
            "additionalProperties": False,
        },
        "languages": {
            "type": "object",
            "properties": {
                "java": {
                    "type": "object",
                    "properties": {
                        "mainClass": {
                            "type": "string",
                        },
                        "taskClass": {
                            "type": "string",
                        },
                    },
                    "required": ["mainClass", "taskClass"],
                },
            },
            "required": ["java"],
            "additionalProperties": False,
        },
        "tests": {
            "type": "array",
            "items": [
                {
                    "type": "object",
                    "properties": {
                        "input": {
                            "type": "string",
                        },
                        "output": {
                            "type": "string",
                        },
                    },
                    "required": ["input", "output"],
                    "additionalProperties": False,
                },
            ],
        },
    },
    "required": [
        "name",
        "group",
        "url",
        "memoryLimit",
        "timeLimit",
        "testType",
        "input",
        "output",
        "tests",
    ],
    "additionalProperties": False,
}


def main(problem: Problem, *, is_system: bool, is_compatibility: bool, is_full: bool, session: requests.Session) -> Dict[str, Any]:
    """
    :raises Exception:
    """

    assert not (is_compatibility and is_full)

    result: Dict[str, Any] = {
        "url": problem.get_url(),
        "tests": [],
    }

    # download test cases
    if is_system:
        tests = problem.download_system_cases(session=session)
    else:
        tests = problem.download_sample_cases(session=session)
    for test in tests:
        data_ = {
            "input": test.input_data.decode(),
            "output": test.output_data.decode(),
        }
        if is_system and not is_compatibility:
            data_['name'] = test.name
        result['tests'].append(data_)

    detail: ProblemData
    contest_detail: ContestData

    # download detailed result
    if isinstance(problem, AtCoderProblem):
        detail = problem.download_data(session=session)
        contest_detail = problem.get_contest().download_data(session=session)
        if is_compatibility:
            result["name"] = '{}. {}'.format(detail.alphabet, detail.name)
            result["group"] = contest_detail.name
        else:
            result["name"] = detail.name
            result["context"] = {
                "contest": {
                    "name": contest_detail.name,
                    "url": problem.get_contest().get_url(),
                },
                "alphabet": detail.alphabet,
            }
        result["memoryLimit"] = detail.memory_limit_byte // 1000 // 1000
        result["timeLimit"] = detail.time_limit_msec
        if is_full:
            result["raw"] = {
                "html": detail.html.decode(),
            }

    elif isinstance(problem, CodeforcesProblem):
        detail = problem.download_data(session=session)
        contest_detail = problem.get_contest().download_data(session=session)
        if is_compatibility:
            result["name"] = '{}. {}'.format(problem.index, detail.name)
            result["group"] = contest_detail.name
        else:
            result["name"] = detail.name
            result["context"] = {
                "contest": {
                    "name": contest_detail.name,
                    "url": problem.get_contest().get_url(),
                },
                "alphabet": problem.index,
            }
        if is_compatibility:
            result["memoryLimit"] = 0
            result["timeLimit"] = 0
        if is_full:
            result["raw"] = {
                "json": detail.json.decode(),
            }

    else:
        if is_compatibility:
            result["name"] = "Z. Dummy Name"
            result["group"] = "Dummy Group"
            result["memoryLimit"] = 0
            result["timeLimit"] = 0
        else:
            result["context"] = {}

    if is_full:
        try:
            available_languages = problem.get_available_languages(session=session)
        except Exception as e:
            logger.warning("failed to list available languages: %s", e)
        else:
            result["availableLanguages"] = []
            for language in available_languages:
                result["availableLanguages"].append({
                    "id": language.id,
                    "description": language.name,
                })

    # add some fields for compatibility
    if is_compatibility:
        result.update({
            "input": {
                "type": "stdin",
            },
            "output": {
                "type": "stdout",
            },
            "testType": "single",
            "languages": {
                "java": {
                    "mainClass": "Main",
                    "taskClass": "Task",
                },
            },
        })

    return result
