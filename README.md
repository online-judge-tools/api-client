# Online Judge API Client

[![test](https://github.com/kmyk/online-judge-api-client/workflows/test/badge.svg)](https://github.com/kmyk/online-judge-api-client/actions)
[![Documentation Status](https://readthedocs.org/projects/online-judge-api-client/badge/?version=master)](https://online-judge-api-client.readthedocs.io/en/master/)
[![PyPI](https://img.shields.io/pypi/v/online-judge-api-client.svg)](https://pypi.python.org/pypi/online-judge-api-client)
[![PyPI](https://img.shields.io/pypi/l/online-judge-api-client.svg)](https://github.com/kmyk/online-judge-api-client/blob/master/LICENSE)


## What is this?

This is an API client for various online judges, used as the backend library of [`oj` command](https://github.com/kmyk/online-judge-tools).
You can use the Python library (`onlinejudge` module) and the command-line interface (`oj-api` command) which talks JSON compatible with [jmerle/competitive-companion](https://github.com/jmerle/competitive-companion).


## How to install

**CAUTION: under developping; this may work stably, but all public APIs are unstable**

``` console
$ git clone https://github.com/kmyk/online-judge-api-client
$ cd online-judge-api-client
$ pip3 install -e .
```


## Supported websites

| website                                                                        | get sample cases   | get system cases   | get metadata       | get contest data   | login service      | submit code        |
|--------------------------------------------------------------------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| [Aizu Online Judge](https://onlinejudge.u-aizu.ac.jp/home)                     | :heavy_check_mark: | :heavy_check_mark: |                    |                    | :white_check_mark: |                    |
| [Anarchy Golf](http://golf.shinh.org/)                                         | :heavy_check_mark: | :white_check_mark: |                    |                    | :white_check_mark: |                    |
| [AtCoder](https://atcoder.jp/)                                                 | :heavy_check_mark: |                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| [CodeChef](https://www.codechef.com/)                                          | :heavy_check_mark: |                    |                    |                    | :white_check_mark: |                    |
| [Codeforces](https://codeforces.com/)                                          | :heavy_check_mark: |                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| [CS Academy](https://csacademy.com/)                                           | :heavy_check_mark: |                    |                    |                    | :white_check_mark: |                    |
| [Facebook Hacker Cup](https://www.facebook.com/hackercup/)                     | :heavy_check_mark: |                    |                    |                    | :white_check_mark: |                    |
| [Google Code Jam](https://codingcompetitions.withgoogle.com/codejam)           | :heavy_check_mark: |                    |                    |                    | :white_check_mark: |                    |
| [Google Kick Start](https://codingcompetitions.withgoogle.com/kickstart)       | :heavy_check_mark: |                    |                    |                    | :white_check_mark: |                    |
| [HackerRank](https://www.hackerrank.com/)                                      | :white_check_mark: | :heavy_check_mark: |                    |                    | :white_check_mark: | :heavy_check_mark: |
| [Kattis](https://open.kattis.com/)                                             | :heavy_check_mark: |                    |                    |                    | :white_check_mark: |                    |
| [Library Checker](https://judge.yosupo.jp/)                                    | :heavy_check_mark: | :heavy_check_mark: |                    |                    | :white_check_mark: |                    |
| [PKU JudgeOnline](http://poj.org/)                                             | :heavy_check_mark: |                    |                    |                    | :white_check_mark: |                    |
| [Sphere Online Judge](https://www.spoj.com/)                                   | :heavy_check_mark: |                    |                    |                    | :white_check_mark: |                    |
| [Toph](https://toph.co/)                                                       | :heavy_check_mark: |                    |                    |                    | :white_check_mark: | :heavy_check_mark: |
| [yukicoder](https://yukicoder.me/)                                             | :heavy_check_mark: | :heavy_check_mark: |                    |                    | :white_check_mark: | :heavy_check_mark: |


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


### `login-service`

TODO: write description here


### `submit-code`

TODO: write description here
