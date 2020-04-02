from typing import *

from onlinejudge.type import *

schema_example = {
    "loggedIn": True,
}  # type: Dict[str, Any]

schema = {
    "type": "object",
    "properties": {
        "loggedIn": {
            "type": "boolean",
        },
    },
    "required": ["loggedIn"],
}  # type: Dict[str, Any]


def main(service: Service, *, username: Optional[str], password: Optional[str], check_only: bool, session: requests.Session) -> Dict[str, Any]:
    """
    :raises Exception:
    :raises LoginError:
    """

    result = {}  # type: Dict[str, Any]
    if check_only:
        assert username is None
        assert password is None
        result["loggedIn"] = service.is_logged_in(session=session)
    else:
        assert username is not None
        assert password is not None

        def get_credentials() -> Tuple[str, str]:
            assert username is not None  # for mypy
            assert password is not None  # for mypy
            return (username, password)

        service.login(get_credentials=get_credentials, session=session)
        result["loggedIn"] = True
    return result
