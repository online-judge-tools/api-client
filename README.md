# online-judge-tools/api-client

[![test](https://github.com/kmyk/online-judge-api-client/workflows/test/badge.svg)](https://github.com/kmyk/online-judge-api-client/actions)
[![Documentation Status](https://readthedocs.org/projects/online-judge-tools/badge/?version=master)](https://online-judge-tools.readthedocs.io/en/master/)
[![PyPI](https://img.shields.io/pypi/v/online-judge-api-client.svg)](https://pypi.python.org/pypi/online-judge-api-client)
[![PyPI](https://img.shields.io/pypi/l/online-judge-api-client.svg)](https://github.com/kmyk/online-judge-api-client/blob/master/LICENSE)


## What is this?

This is an API client for various online judges, used as the backend library of [`oj` command](https://github.com/kmyk/online-judge-tools).
You can use the Python library (`onlinejudge` module) and the command-line interface (`oj-api` command) which talks JSON compatible with [jmerle/competitive-companion](https://github.com/jmerle/competitive-companion).


## How to install

``` console
$ pip3 install online-judge-api-client
```


## Supported websites

| website                                                                        | get sample cases   | get system cases   | get metadata       | get contest data   | login service      | submit code        |
|--------------------------------------------------------------------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| [Aizu Online Judge](https://onlinejudge.u-aizu.ac.jp/home)                     | :heavy_check_mark: | :heavy_check_mark: |                    |                    |                    |                    |
| [Anarchy Golf](http://golf.shinh.org/)                                         | :heavy_check_mark: | :grey_question: (same to samples) |                    |                    |                    |                    |
| [AtCoder](https://atcoder.jp/)                                                 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| [AtCoder Problems](https://kenkoooo.com/atcoder) (virtual contests)            |                    |                    |                    | :heavy_check_mark: |                    |                    |
| [CodeChef](https://www.codechef.com/)                                          | :heavy_check_mark: |                    | :heavy_check_mark: | :heavy_check_mark: | :grey_question:    |                    |
| [Codeforces](https://codeforces.com/)                                          | :heavy_check_mark: |                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: [issue](https://github.com/online-judge-tools/api-client/issues/127) |
| [CS Academy](https://csacademy.com/)                                           | :heavy_check_mark: |                    |                    |                    |                    |                    |
| [Facebook Hacker Cup](https://www.facebook.com/hackercup/)                     | :heavy_check_mark: |                    |                    |                    |                    |                    |
| [Google Code Jam](https://codingcompetitions.withgoogle.com/codejam)           | :heavy_check_mark: |                    |                    |                    |                    |                    |
| [Google Kick Start](https://codingcompetitions.withgoogle.com/kickstart)       | :heavy_check_mark: |                    |                    |                    |                    |                    |
| [HackerRank](https://www.hackerrank.com/)                                      | :heavy_check_mark: | :heavy_check_mark: |                    |                    | :grey_question: | :heavy_check_mark: |
| [Kagamiz Contest System](https://kcs.miz-miz.biz/)                             | :x:                |                    |                    |                    | :grey_question:    | :heavy_check_mark: |
| [Kattis](https://open.kattis.com/)                                             | :heavy_check_mark: |                    |                    |                    |                    |                    |
| [Library Checker](https://judge.yosupo.jp/)                                    | :heavy_check_mark: | :heavy_check_mark: |                    |                    |                    |                    |
| [PKU JudgeOnline](http://poj.org/)                                             | :heavy_check_mark: |                    |                    |                    |                    |                    |
| [Sphere Online Judge](https://www.spoj.com/)                                   | :heavy_check_mark: |                    |                    |                    |                    |                    |
| [Topcoder](https://arena.topcoder.com/)                                        | :heavy_check_mark: (archived problems only) |                    | :grey_question: |                    |                    |                    |
| [Toph](https://toph.co/)                                                       | :heavy_check_mark: |                    |                    |                    | :grey_question: | :heavy_check_mark: |
| [yukicoder](https://yukicoder.me/)                                             | :heavy_check_mark: | :heavy_check_mark: |                    | :heavy_check_mark: | :grey_question: | :heavy_check_mark: |

Instead of `login-service`, you can use [`oj` command](https://github.com/online-judge-tools/oj) with Selenium as `oj login https://...`. This can login almost all services.


## Supported subcommands of `oj-api` command

### `get-problem`

`oj-api get-problem PROBLEM_URL` parses the given problem and prints the results as JSON compatible with [jmerle/competitive-companion](https://github.com/jmerle/competitive-companion).


#### options

-   `--system`: get system cases, instead of sample cases
-   `--full`: dump all additional data


#### format

-   `url`: the URL of the problem
-   `name`: the name of the problem. This doesn't include alphabets (e.g. just "Xor Sum" is used instead of "D. Xor Sum") because such alphabets are attributes belonging to the relation between problems and contests rather than belonging to only problems. (not compatible to [jmerle/competitive-companion](https://github.com/jmerle/competitive-companion))
-   `context`:
    -    `contest` (optional):
        -    `url`: the URL of the contest
        -    `name`: the name of the contest
    -    `alphabet` (optional): the alphabet of the problem in the contest
-   `memoryLimit`: the memory limit in megabytes (MB); not mebibytes (MiB). They sometimes become non-integers, but be rounded down for the compatibility reason with [jmerle/competitive-companion](https://github.com/jmerle/competitive-companion).
-   `timeLimit`: the time limit in milliseconds (msec)
-   `tests`:
    -   `input`: the input of the test case
    -   `output`: the output of the test case


#### format (additional)

-   `tests`:
    -   `name` (optional, when `--system`): the name of the system case (e.g. `random-004.in`, `fft_killer_01`, `99_hand.txt`)
-   `availableLanguages` (optional, when `--full`):
    -   `id`: the ID of language to submit the server (e.g. `3003`)
    -   `description`: the description of the language to show to users (e.g. `C++14 (GCC 5.4.1)`)
-   `raw` (optional, when `--full`):
    -   `html` (optional): the raw HTML used internally. This might contain sensitive info like CSRF tokens.
    -   `json` (optional): the raw JSON used internally. This might contain sensitive info like access tokens.
    -   etc.


#### example

``` json
$ oj-api get-problem https://atcoder.jp/contests/arc100/tasks/arc100_b | jq .result
{
  "url": "https://atcoder.jp/contests/arc100/tasks/arc100_b",
  "name": "Equal Cut",
  "context": {
    "contest": {
      "url": "https://atcoder.jp/contests/arc100",
      "name": "AtCoder Regular Contest 100"
    },
    "alphabet": "D"
  },
  "memoryLimit": 1024,
  "timeLimit": 2000,
  "tests": [
    {
      "input": "5\n3 2 4 1 2\n",
      "output": "2\n"
    },
    {
      "input": "10\n10 71 84 33 6 47 23 25 52 64\n",
      "output": "36\n"
    },
    {
      "input": "7\n1 2 3 1000000000 4 5 6\n",
      "output": "999999994\n"
    }
  ]
}
```


### `get-problem --compatibility`

`oj-api get-problem --compatibility PROBLEM_URL` is the variant of `get-problem` strictly compatible with [jmerle/competitive-companion](https://github.com/jmerle/competitive-companion).


#### format

See the document of [jmerle/competitive-companion](https://github.com/jmerle/competitive-companion).


#### example

``` json
{
  "name": "D. Equal Cut",
  "group": "AtCoder Regular Contest 100",
  "url": "https://atcoder.jp/contests/arc100/tasks/arc100_b",
  "interactive": false,
  "memoryLimit": 1024,
  "timeLimit": 2000,
  "tests": [
    {
      "input": "5\n3 2 4 1 2\n",
      "output": "2\n"
    },
    {
      "input": "10\n10 71 84 33 6 47 23 25 52 64\n",
      "output": "36\n"
    },
    {
      "input": "7\n1 2 3 1000000000 4 5 6\n",
      "output": "999999994\n"
    }
  ],
  "testType": "single",
  "input": {
    "type": "stdin"
  },
  "output": {
    "type": "stdout"
  },
  "languages": {
    "java": {
      "mainClass": "Main",
      "taskClass": "Task"
    }
  }
}
```


### `get-contest`

`oj-api get-contest CONTEST_URL` parses the given contest and prints the results as JSON.


#### format

-   `url`: the URL of the contest
-   `name`: the name of the contest
-   `problems`: problems. For details, see the description of `get-problem`.


#### example

``` json
$ oj-api get-contest https://atcoder.jp/contests/arc100 | jq .result
{
  "url": "https://atcoder.jp/contests/arc100",
  "name": "AtCoder Regular Contest 100",
  "problems": [
    {
      "url": "https://atcoder.jp/contests/arc100/tasks/arc100_a",
      "name": "Linear Approximation",
      "context": {
        "contest": {
          "url": "https://atcoder.jp/contests/arc100",
          "name": "AtCoder Regular Contest 100"
        },
        "alphabet": "C"
      }
    },
    {
      "url": "https://atcoder.jp/contests/arc100/tasks/arc100_b",
      "name": "Equal Cut",
      "context": {
        "contest": {
          "url": "https://atcoder.jp/contests/arc100",
          "name": "AtCoder Regular Contest 100"
        },
        "alphabet": "D"
      }
    },
    {
      "url": "https://atcoder.jp/contests/arc100/tasks/arc100_c",
      "name": "Or Plus Max",
      "context": {
        "contest": {
          "url": "https://atcoder.jp/contests/arc100",
          "name": "AtCoder Regular Contest 100"
        },
        "alphabet": "E"
      }
    },
    {
      "url": "https://atcoder.jp/contests/arc100/tasks/arc100_d",
      "name": "Colorful Sequences",
      "context": {
        "contest": {
          "url": "https://atcoder.jp/contests/arc100",
          "name": "AtCoder Regular Contest 100"
        },
        "alphabet": "F"
      }
    }
  ]
}
```


### `get-service`

`oj-api get-service SERVICE_URL` prints the data of the service.


#### options

-   `--list-contests`: list all contests in the service


#### format

-   `url`: the URL of the service
-   `name`: the name of the service
-   `contests` (when `--list-contests`): contests. For details, see the description of `get-problem`.


#### example

``` json
$ oj-api get-service https://atcoder.jp/ --list-contests | jq .result
{
  "url": "https://atcoder.jp/",
  "name": "AtCoder",
  "contests": [
    {
      "url": "https://atcoder.jp/contests/abc162",
      "name": "AtCoder Beginner Contest 162"
    },
    {
      "url": "https://atcoder.jp/contests/judge-update-202004",
      "name": "Judge System Update Test Contest 202004"
    },
    {
      "url": "https://atcoder.jp/contests/abc161",
      "name": "AtCoder Beginner Contest 161"
    },
    {
      "url": "https://atcoder.jp/contests/abc160",
      "name": "AtCoder Beginner Contest 160"
    },
    ...
  ]
}
```


### `login-service`

`USERNAME=USERNAME PASSWORD=PASSWORD oj-api login-service SERVICE_URL` logs in the given service.


#### options

-   `--check`: only check whether you are already logged in, without trying to log in

#### format

-   `loggedIn`: the result


#### example

``` json
$ USERNAME=kimiyuki PASSWORD='????????????????' oj-api login-service https://atcoder.jp/ | jq .result
{
  "loggedIn": true
}
```


### `submit-code`

`oj-api submit-code PROBLEM_URL --file FILE --language LANGUAGE_ID` submits the file to the given problem.
You can obtrain the `LANGUAGE_ID` from the list `availableLanguages` of `oj-api get-problem --full PROBLEM_URL` or the `guess-language-id` subcommand.


#### format

-   `url`: the URL of the submission result


#### example

``` json
$ oj-api submit-code https://atcoder.jp/contests/abc160/tasks/abc160_a --file main.py --language 3023 | jq .result
{
  "url": "https://atcoder.jp/contests/abc160/submissions/11991846"
}
```


### `guess-language-id`

`oj-api guess-language-id PROBLEM_URL --file FILE` guesses the language id to submit the file to the given problem.


#### format

-   `id`: the language id
-   `description`: the description of the language id


#### example

``` json
$ oj-api guess-language-id http://codeforces.com/contest/1373/problem/A --file=main.py | jq .result
{
  "id": "31",
  "description": "Python 3.7.2",
}
```


## JSON API responses

### format

-   `status`: the status. This contains `ok` if the subcommand succeeded.
-   `messages`: error messages
-   `result`: the result


### example

``` json
$ USERNAME=chokudai PASSWORD=hoge oj-api login-service https://atcoder.jp/ | jq .
{
  "status": "error",
  "messages": [
    "onlinejudge.type.LoginError: failed to login"
  ],
  "result": null
}
```


## Tips

For end-users who don't develop any programs:

-   Please use the [`oj` command](https://github.com/online-judge-tools/oj) instead of this `oj-api` command.
    -   The `oj-api` command is intended to be used as a backend of other programs. It's not a frontend which humans use directly.

For developers of programs which use `oj-api`:

-   Please be polite to judge servers.
    -   We are accessing the web pages using the unintended way, i.e. without GUI browsers. We should not forget that this is basically not welcomed.
-   Please be aware that this package uses [Semantic Versioning](https://semver.org/).
    -   The "public API" of this package is the documented features of `oj-api` command and the [documented modules](https://online-judge-tools.readthedocs.io/en/master/) of `onlinejudge` module.
-   You can also use the `oj login` command to login servers with GUI browsers.
    -   The implementation around authentication is very complicated and fragile. For example, Codeforces has four methods to login: password, Gmail, Facebook, and ICPC. So we need to use GUI browsers for the development cost and stability.
    -   This feature of `oj login` might be imported to `oj-api` command in the future.
