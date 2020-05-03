#!/bin/bash
replace='
    s/\(import\|from\) onlinejudge\>/\1 onlinejudge_workaround_for_conflict/
    /\('\''\|"\).*onlinejudge/ ! {
        s/\<onlinejudge\.\(\w\+\)/onlinejudge_workaround_for_conflict.\1/g
    }
'

for src in $(find onlinejudge -name \*.py) onlinejudge/py.typed ; do
    dst=${src/onlinejudge/onlinejudge_workaround_for_conflict}
    mkdir -p $(dirname $dst)
    sed "$replace" < $src > $dst
done

for src in $(find tests -name \*.py)  ; do
    dst=${src/tests/tests_workaround_for_conflict}
    mkdir -p $(dirname $dst)
    sed "$replace" < $src > $dst
done
