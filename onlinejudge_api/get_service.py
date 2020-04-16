from logging import getLogger
from typing import *

from onlinejudge.type import *

logger = getLogger()

schema_example = {
    "url": "https://atcoder.jp/",
    "name": "AtCoder",
    "contests": [
        {
            "url": "https://atcoder.jp/contests/agc001",
            "name": "AtCoder Grand Contest 001",
        },
        {
            "url": "https://atcoder.jp/contests/agc002",
            "name": "AtCoder Grand Contest 002",
        },
        {
            "url": "https://atcoder.jp/contests/agc003",
            "name": "AtCoder Grand Contest 003",
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
        },
        "contests": {
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
                },
                "required": ["url", "name"],
            },
        },
    },
    "required": [
        "url",
        "name",
    ],
}  # type: Dict[str, Any]


def main(service: Service, *, does_list_contests: bool, session: requests.Session) -> Dict[str, Any]:
    """
    :raises Exception:
    """

    result = {
        "url": service.get_url(),
        "name": service.get_name(),
    }  # type: Dict[str, Any]

    if does_list_contests:
        contests = []
        for contest in service.iterate_contests(session=session):
            contests.append({
                "url": contest.get_url(),
                "name": contest.download_data().name,
            })
        result['contests'] = contests

    return result
