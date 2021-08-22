# Change Log

## 10.10.0 / 2021-08-23

-   [#144](https://github.com/online-judge-tools/api-client/pull/144) add CodeChef support again

## 10.9.0 / 2021-04-23

-   [#139](https://github.com/online-judge-tools/api-client/pull/139) support downloading system cases from AtCoder (helped by [@qryxip](https://github.com/qryxip))

## 10.8.0 / 2021-01-19

-   [#133](https://github.com/online-judge-tools/api-client/pull/133) allow [old.yosupo.jp](https://old.yosupo.jp/) as URLs for Library-Checker problems
-   [#134](https://github.com/online-judge-tools/api-client/pull/134) support virtual contests of [AtCoder Problems](https://kenkoooo.com/atcoder)
-   [#135](https://github.com/online-judge-tools/api-client/pull/135) update about `get-contest` subcommand; support yukicoder contests

## 10.7.1 / 2020-12-25

-   [#130](https://github.com/online-judge-tools/api-client/pull/130) fix an error on submissions to HackerRank ([@wapa5pow](https://github.com/wapa5pow))

## 10.7.0 / 2020-12-18

-   [#128](https://github.com/online-judge-tools/api-client/pull/128) [breaking changes] remove the feature to submit code to Codeforces
    -   The reason is described at [#127](https://github.com/online-judge-tools/api-client/issues/127)

## 10.6.1 / 2020-12-15

-   [#125](https://github.com/online-judge-tools/api-client/pull/125) fix an issue about submissions to Codeforces again

## 10.6.0 / 2020-11-25

-   [#116](https://github.com/online-judge-tools/api-client/pull/116) [breaking changes] finished Python 3.5 support
    -   This breaks some environments, but such environments already reached EOL. The major version is not incremented.
-   [#120](https://github.com/online-judge-tools/api-client/pull/120) fix an issue about submissions to Codeforces

## 10.5.0 / 2020-10-14

-   [#112](https://github.com/online-judge-tools/api-client/pull/112) deprecate the feature to get detailed info from submissions on AtCoder. The code is broken by update of AtCoder and replaced with placeholders.
-   [#111](https://github.com/online-judge-tools/api-client/pull/111) fix some features about yukicoder

## 10.4.0 / 2020-09-22

-   [#106](https://github.com/online-judge-tools/api-client/pull/106) add support for Kagamiz Contest System

## 10.3.3 / 2020-08-30

-   [#103](https://github.com/online-judge-tools/api-client/pull/103) fix an issue about submitting code to Codeforces

## 10.3.2 / 2020-08-24

-   [#99](https://github.com/online-judge-tools/api-client/pull/99) fix the parser of AtCoder to work even when a user is logged in as an admin  ([@yosupo06](https://github.com/yosupo06))

## 10.3.1 / 2020-08-21

-   [#98](https://github.com/online-judge-tools/api-client/pull/98) tweak the testcases downloader for HackerRank
-   [#97](https://github.com/online-judge-tools/api-client/pull/97) remove deprecated methods for yukicoder which are newly broken
-   [#95](https://github.com/online-judge-tools/api-client/pull/95) support Codeforces EDU problems  ([@aberent](https://github.com/aberent))
-   [#93](https://github.com/online-judge-tools/api-client/pull/93) fix the sample downloader for Facebook Hacker Cup
-   [#91](https://github.com/online-judge-tools/api-client/pull/91) add the contest parser for yukicoder

## 10.3.0 / 2020-08-13

-   [#61](https://github.com/online-judge-tools/api-client/issues/61) [#68](https://github.com/online-judge-tools/api-client/pull/68) improve the logging for clients of this library

## 10.2.6 / 2020-08-08

-   [#86](https://github.com/online-judge-tools/api-client/issues/86) fix the breakage of the parser of AtCoder
-   [#84](https://github.com/online-judge-tools/api-client/issues/84) remove the feature for Facebook Hacker Cup

## 10.2.5 / 2020-07-24

-   [#82](https://github.com/online-judge-tools/api-client/pull/82) fix the bug that happens when GCJ has multiple samples ([@queragion2726](https://github.com/queragion2726))

## 10.2.4 / 2020-07-16

-   [#80](https://github.com/online-judge-tools/api-client/pull/80) revert the patch for RCPC tokens of Codeforces

## 10.2.3 / 2020-07-15

-   [#78](https://github.com/online-judge-tools/api-client/pull/78) fix the issue of Codeforces partially using RCPC tokens (helped by [@9kin](https://github.com/9kin))

## 10.2.2 / 2020-07-14

-   [#74](https://github.com/online-judge-tools/api-client/pull/74) disable the login feature for Codeforces
-   [#58](https://github.com/online-judge-tools/api-client/pull/58) [breaking changes] remove deprecated APIs for yukicoder

## 10.2.1 / 2020-06-30

-   [#71](https://github.com/online-judge-tools/api-client/pull/71) fix the login feature for yukicoder ([@beet-aizu](https://github.com/beet-aizu))

## 10.2.0 / 2020-06-30

-   [#63](https://github.com/online-judge-tools/api-client/pull/63) add `guess-language-id` subcommand as a utility
-   [#66](https://github.com/online-judge-tools/api-client/pull/66) print the version info for user support

## 10.1.1 / 2020-06-06

-   [#56](https://github.com/online-judge-tools/api-client/pull/56) remove trailing spaces from sample cases of Codeforces
-   [#57](https://github.com/online-judge-tools/api-client/pull/57) fix a problem of `oj-api login-service` on Zsh

## 10.1.0 / 2020-05-22

-   [#47](https://github.com/online-judge-tools/api-client/pull/47) add Topcoder support only for archived problems
-   [#50](https://github.com/online-judge-tools/api-client/pull/50) remove CodeChef support

## 10.0.8 / 2020-05-07

-   [#43](https://github.com/online-judge-tools/api-client/pull/43) add a workaround for the another issue about installation
-   [#42](https://github.com/online-judge-tools/api-client/pull/42) fix a workaround

## 10.0.7 / 2020-05-05

-   [#35](https://github.com/online-judge-tools/api-client/pull/35) add `colorlog` to dependencies for Library Checker ([@yosupo06](https://github.com/yosupo06))

## 10.0.6 / 2020-05-04

-   [#33](https://github.com/online-judge-tools/api-client/pull/33) fix the workaround added at v10.0.5
-   [#32](https://github.com/online-judge-tools/api-client/pull/32) fix the bug about the default cookie path

## 10.0.5 / 2020-05-04

-   [#30](https://github.com/online-judge-tools/api-client/pull/30) add another workaround for the same problem to 10.0.3

## 10.0.4 / 2020-05-04

-   [#28](https://github.com/online-judge-tools/api-client/pull/28) fix the workaround added at 10.0.3

## 10.0.3 / 2020-05-04

-   [#26](https://github.com/online-judge-tools/api-client/pull/26) add a workaround for a problem about installation

## 10.0.2 / 2020-05-01

-   [online-judge-tools/oj#738](https://github.com/online-judge-tools/oj/pull/738) fix the lack of the support for a URL format of AOJ ([@knshnb](https://github.com/knshnb))

## 10.0.1 / 2020-05-02

-   [#12](https://github.com/online-judge-tools/api-client/pull/12) fix bugs of the module for Codeforces
-   [#10](https://github.com/online-judge-tools/api-client/pull/10) add type hints info to the Python package

## 10.0.0 / 2020-05-02

-   forked from [online-judge-tools](https://github.com/kmyk/online-judge-tools) `v9.2.2`
-   add `oj-api` command
