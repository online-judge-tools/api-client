# Contribution and Hacking Guide

links:

-   [CONTRIBUTING.md](https://github.com/online-judge-tools/.github/blob/master/CONTRIBUTING.md) of [online-judge-tools](https://github.com/online-judge-tools) organization
-   [DESIGN.md](https://github.com/online-judge-tools/api-client/blob/master/DESIGN.md)


## For committer of `oj-api` command / `oj-api` コマンド本体への貢献者へ

-   Please read [CONTRIBUTING.md](https://github.com/online-judge-tools/.github/blob/master/CONTRIBUTING.md).


### How to add a new online judge service

Do following steps:

1.  Make a file `onlinejudge/service/YOUR_SERVICE.py` in a way similar to other files
    -   Implement a subclass of `onlinejudge.type.Service`
    -   Implement a subclass of `onlinejudge.type.Problem`
1.  Register the module to `onlinejudge/service/__init__.py`
1.  Add tests to `tests/`
1.  Update documents like `README.md`


## For developpers of programs which uses `oj-api` command / `oj-api` コマンドを用いたツールの開発者へ

-   For the JSON interface, the document exist at [README.md](https://github.com/online-judge-tools/api-client/blob/master/README.md).
-   You should know the existence of [jmerle/competitive-companion](https://github.com/jmerle/competitive-companion). We recommend you to write programs which accept JSON from both API clients.
