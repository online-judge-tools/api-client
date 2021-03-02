import onlinejudge.dispatch as dispatch
from onlinejudge_api.main import main


def is_logged_in(url: str, *, memo={}) -> bool:
    # functools.lru_cache is unusable since Service are unhashable, so we need to use `memo={}`.
    service = dispatch.service_from_url(url)
    assert service is not None
    url = service.get_url()  # normalize url
    if url not in memo:
        # We need to use main instead of `service.is_logged_in()` to use cookies.
        result = main(['login-service', '--check', url], debug=True)
        memo[url] = bool((result.get('result') or {}).get('loggedIn'))
    return memo[url]
