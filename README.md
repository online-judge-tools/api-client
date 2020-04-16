# Online Judge API Client


[![test](https://github.com/kmyk/online-judge-api-client/workflows/test/badge.svg)](https://github.com/kmyk/online-judge-api-client/actions)
[![Documentation Status](https://readthedocs.org/projects/online-judge-api-client/badge/?version=master)](https://online-judge-api-client.readthedocs.io/en/master/)
[![PyPI](https://img.shields.io/pypi/v/online-judge-api-client.svg)](https://pypi.python.org/pypi/online-judge-api-client)
[![PyPI](https://img.shields.io/pypi/l/online-judge-api-client.svg)](https://github.com/kmyk/online-judge-api-client/blob/master/LICENSE)

## Examples

``` json
$ oj-api get-problem https://atcoder.jp/contests/arc100/tasks/arc100_b | jq .result
{
  "url": "https://atcoder.jp/contests/arc100/tasks/arc100_b",
  "name": "Equal Cut",
  "context": {
    "contest": {
      "name": "AtCoder Regular Contest 100",
      "url": "https://atcoder.jp/contests/arc100"
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
          "name": "AtCoder Regular Contest 100",
          "url": "https://atcoder.jp/contests/arc100"
        },
        "alphabet": "C"
      }
    },
    {
      "url": "https://atcoder.jp/contests/arc100/tasks/arc100_b",
      "name": "Equal Cut",
      "context": {
        "contest": {
          "name": "AtCoder Regular Contest 100",
          "url": "https://atcoder.jp/contests/arc100"
        },
        "alphabet": "D"
      }
    },
    {
      "url": "https://atcoder.jp/contests/arc100/tasks/arc100_c",
      "name": "Or Plus Max",
      "context": {
        "contest": {
          "name": "AtCoder Regular Contest 100",
          "url": "https://atcoder.jp/contests/arc100"
        },
        "alphabet": "E"
      }
    },
    {
      "url": "https://atcoder.jp/contests/arc100/tasks/arc100_d",
      "name": "Colorful Sequences",
      "context": {
        "contest": {
          "name": "AtCoder Regular Contest 100",
          "url": "https://atcoder.jp/contests/arc100"
        },
        "alphabet": "F"
      }
    }
  ]
}
```
