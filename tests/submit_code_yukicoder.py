import os
import pathlib
import tempfile
import textwrap
import unittest

from onlinejudge_api.main import main

YUKICODER_TOKEN = os.environ.get('YUKICODER_TOKEN')


@unittest.skipIf(YUKICODER_TOKEN is None, '$YUKICODER_TOKEN is required')
class SubmitYukicoderTest(unittest.TestCase):
    def test_9000(self):
        url = 'https://yukicoder.me/problems/no/9000'
        filename = 'main.py'
        code = textwrap.dedent(r"""
            #!/usr/bin/env python3
            print "Hello World!"
        """)

        with tempfile.TemporaryDirectory() as tempdir:
            path = pathlib.Path(tempdir) / filename
            with open(path, 'w') as fh:
                fh.write(code)
            language_id = main(['guess-language-id', '--file', str(path), url], debug=True)['result']['id']
            data = main(['submit-code', '--file', str(path), '--language', language_id, url], debug=True)
            self.assertEqual(data['status'], 'ok')

    def test_527(self):
        url = 'https://yukicoder.me/problems/527'
        filename = 'main.cpp'
        code = textwrap.dedent(r"""
            #include <bits/stdc++.h>
            using namespace std;
            int main() {
                int a, b; cin >> a >> b;
                string s; cin >> s;
                cout << a + b << ' ' << s << endl;
                return 0;
            }
        """)

        with tempfile.TemporaryDirectory() as tempdir:
            path = pathlib.Path(tempdir) / filename
            with open(path, 'w') as fh:
                fh.write(code)
            language_id = main(['guess-language-id', '--file', str(path), url], debug=True)['result']['id']
            data = main(['submit-code', '--file', str(path), '--language', language_id, url], debug=True)
            self.assertEqual(data['status'], 'ok')
