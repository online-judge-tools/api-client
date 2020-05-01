import pathlib
from typing import *

from onlinejudge.type import *

schema_example = {
    "url": "https://atcoder.jp/contests/abc158/submissions/10899822",
}  # type: Dict[str, Any]

schema = {
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
            "format": "uri",
        },
    },
    "required": ["url"],
}  # type: Dict[str, Any]


def main(problem: Problem, *, file: pathlib.Path, language_id: LanguageId, session: requests.Session) -> Dict[str, Any]:
    """
    :raises NotLoggedInError:
    :raises SubmissionError:
    :raises NotImplementedError:
    """

    with open(str(file), "rb") as fh:
        code = fh.read()
    submission = problem.submit_code(code, language_id=language_id, filename=str(file), session=session)

    result = {
        "url": submission.get_url(),
    }  # type: Dict[str, Any]
    return result
