from onlinejudge_api.main import main

from onlinejudge.type import Service


def is_logged_in(service: Service, *, memo={}) -> bool:
    # functools.lru_cache is unusable since Service are unhashable, so we need to use `memo={}`.
    url = service.get_url()
    if url not in memo:
        # We need to use main instead of `service.is_logged_in()` to use cookies.
        result = main(['login-service', '--check', url], debug=True)
        memo[url] = bool((result.get('result') or {}).get('loggedIn'))
    return memo[url]
