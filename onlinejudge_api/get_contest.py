from typing import *

from onlinejudge.service.atcoder import AtCoderContest
from onlinejudge.service.codeforces import CodeforcesContest
from onlinejudge.type import *

schema_example: Dict[str, Any] = {
    "url": "https://atcoder.jp/contests/cf16-exhibition",
    "name": "CODE FESTIVAL 2016 Exhibition",
    "problems": [
        {
            "url": "https://atcoder.jp/contests/cf16-exhibition/tasks/codefestival_2016_ex_a",
            "name": "Distance Pairs",
            "context": {
                "contest": {
                    "url": "https://atcoder.jp/contests/cf16-exhibition",
                    "name": "CODE FESTIVAL 2016 Exhibition",
                },
                "alphabet": "A",
            }
        },
        {
            "url": "https://atcoder.jp/contests/cf16-exhibition/tasks/codefestival_2016_ex_b",
            "name": "Exact Payment",
            "context": {
                "contest": {
                    "url": "https://atcoder.jp/contests/cf16-exhibition",
                    "name": "CODE FESTIVAL 2016 Exhibition",
                },
                "alphabet": "B",
            }
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
        "problems": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "format": "uri",
                    },
                    "name": {
                        "type": "string",
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
                },
                "required": ["url", "name", "context"],
            },
        },
    },
    "required": ["url", "problems"],
}


def main(contest: Contest, *, is_full: bool, session: requests.Session) -> Dict[str, Any]:
    """
    :raises Exception:
    """

    data: Dict[str, Any] = {
        "url": contest.get_url(),
        "problems": [],
    }

    detail: ContestData
    problem_data: ProblemData
    problem: Problem
    data_: Dict[str, Any]

    if isinstance(contest, AtCoderContest):
        detail = contest.download_data(session=session)
        data["name"] = detail.name
        for problem_data in contest.list_problem_data(session=session):
            problem = problem_data.problem
            data_ = {
                "url": problem.get_url(),
                "name": problem_data.name,
                "context": {
                    "contest": {
                        "name": detail.name,
                        "url": contest.get_url(),
                    },
                    "alphabet": problem_data.alphabet,
                },
            }
            data["problems"].append(data_)
        if is_full:
            data["raw"] = {
                "html": detail.html.decode(),
            }

    elif isinstance(contest, CodeforcesContest):
        detail = contest.download_data(session=session)
        data["name"] = detail.name
        for problem_data in contest.list_problem_data(session=session):
            problem = problem_data.problem
            data_ = {
                "url": problem.get_url(),
                "name": problem_data.name,
                "context": {
                    "contest": {
                        "name": detail.name,
                        "url": contest.get_url(),
                    },
                    "alphabet": problem.index,
                },
            }
            data["problems"].append(data_)
        if is_full:
            data["raw"] = {
                "json": detail.json.decode(),
            }

    else:
        assert False

    return data
