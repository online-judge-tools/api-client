from logging import getLogger
from typing import *

from onlinejudge.service.atcoder import AtCoderProblem
from onlinejudge.service.codeforces import CodeforcesProblem
from onlinejudge.service.topcoder import TopcoderProblem
from onlinejudge.type import *

logger = getLogger()

schema_example = {
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
}  # type: Dict[str, Any]

schema = {
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
            "description": "in megabytes (MB), not in mebibytes (MiB); Decimals are truncated for compatibility to competitive-companion",
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
}  # type: Dict[str, Any]

schema_compatibility = {
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
}  # type: Dict[str, Any]


def translate_to_competitive_companion_format(data: Dict[str, Any]) -> Dict[str, Any]:
    name = "{}. {}".format(data["context"].get("alphabet", "Z"), data.get("name", "Dummy Name"))
    group = data["context"].get("contest", {}).get("name", "Dummy Group")
    url = data["url"]
    memory_limit = data.get("memoryLimit", 0)
    time_limit = data.get("timeLimit", 0)
    tests = [{"input": test["input"], "output": test["output"]} for test in data["tests"]]
    return {
        "name": name,
        "group": group,
        "url": url,
        "interactive": False,
        "memoryLimit": memory_limit,
        "timeLimit": time_limit,
        "tests": tests,
        "testType": "single",
        "input": {
            "type": "stdin",
        },
        "output": {
            "type": "stdout",
        },
        "languages": {
            "java": {
                "mainClass": "Main",
                "taskClass": "Task",
            },
        },
    }


def main(problem: Problem, *, is_system: bool, is_compatibility: bool, is_full: bool, session: requests.Session) -> Dict[str, Any]:
    """
    :raises Exception:
    """

    result = {
        "url": problem.get_url(),
        "tests": [],
    }  # type: Dict[str, Any]

    # download test cases
    if is_system:
        tests = problem.download_system_cases(session=session)
    else:
        tests = problem.download_sample_cases(session=session)
    for test in tests:
        result_ = {
            "input": test.input_data.decode(),
            "output": test.output_data.decode(),
        }
        if is_system:
            result_['name'] = test.name
        result['tests'].append(result_)

    # download detailed result
    data = None  # type: Optional[ProblemData]
    contest_data = None  # type: Optional[ContestData]
    if isinstance(problem, AtCoderProblem):
        data = problem.download_data(session=session)
        contest_data = problem.get_contest().download_data(session=session)
        result["name"] = data.name
        result["context"] = {
            "contest": {
                "name": contest_data.name,
                "url": problem.get_contest().get_url(),
            },
            "alphabet": data.alphabet,
        }
        result["memoryLimit"] = data.memory_limit_byte // 1000 // 1000
        result["timeLimit"] = data.time_limit_msec
        if is_full:
            result["raw"] = {
                "html": data.html.decode(),
            }

    elif isinstance(problem, CodeforcesProblem) and problem.kind not in {'problemset', 'edu'}:
        try:
            data = problem.download_data(session=session)
        except Exception as e:
            logger.exception(e)
        try:
            contest_data = problem.get_contest().download_data(session=session)
        except Exception as e:
            logger.exception(e)
        result["context"] = {
            "contest": {
                "url": problem.get_contest().get_url(),
            },
            "alphabet": problem.index,
        }
        if data is not None:
            result["name"] = data.name
        if contest_data is not None:
            result["context"]["contest"]["name"] = contest_data.name
        if is_full:
            if data is not None and data.json is not None:
                result["raw"] = {
                    "json": data.json.decode(),
                }

    elif isinstance(problem, TopcoderProblem):
        definition = problem._download_data(session=session).definition
        result["name"] = definition["class"]
        if is_full:
            result["raw"] = {
                "definition": definition,
            }

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

    if is_compatibility:
        return translate_to_competitive_companion_format(result)
    else:
        return result
