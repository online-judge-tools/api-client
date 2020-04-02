import pathlib
from typing import *

from onlinejudge.type import *

schema_example: Dict[str, Any] = {
    "url": "https://atcoder.jp/contests/abc158/submissions/10899822",
}

schema: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
            "format": "uri",
        },
    },
    "required": ["url"],
}


def main(problem: Problem, *, file: pathlib.Path, language_id: LanguageId, session: requests.Session) -> Dict[str, Any]:
    """
    :raises NotLoggedInError:
    :raises SubmissionError:
    :raises NotImplementedError:
    """

    with open(str(file), "rb") as fh:
        code = fh.read()
    submission = problem.submit_code(code, language_id=language_id, filename=str(file), session=session)

    problem_detail = problem.download_data(session=session)
    result: Dict[str, Any] = {
        "url": submission.get_url(),
    }
    return result
