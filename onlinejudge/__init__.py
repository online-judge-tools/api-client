"""
isort: skip_file
"""

# This is a workaround for the issue https://github.com/online-judge-tools/oj/issues/771
# You can reproduce this issue with:
#     $ pip3 uninstall online-judge-tools online-judge-api-client
#     $ pip3 install online-judge-tools==9.2.2
#     $ pip3 install online-judge-api-client
# pylint: disable=unused-import,ungrouped-imports
try:
    import onlinejudge._implementation.main  # type: ignore
except ImportError:
    pass
else:
    import sys
    import textwrap
    print(textwrap.dedent("""\
        You use an old version of online-judge-tools (< 10.0.0) with online-judge-api-client, they are not compatible.
        Please execute:

            1. Uninstall online-judge-tools and online-judge-api-client.
                $ pip3 uninstall online-judge-tools online-judge-api-client

            2. Check if they are completely uninstalled. It has successfully uninstalled when the following commands say something like "not found".
                $ command oj
                oj: command not found

                $ python3 -c 'from onlinejudge.__about__ import __version__ ; print(__version__)'
                Traceback (most recent call last):
                  File "<string>", line 1, in <module>
                ModuleNotFoundError: No module named 'onlinejudge.__about__'

            3. Reinstall online-judge-tools.
                $ pip3 install online-judge-tools"""), file=sys.stderr)
    sys.exit(1)
# pylint: enable=unused-import,ungrouped-imports

import onlinejudge.dispatch
import onlinejudge.service
from onlinejudge.__about__ import __version__
