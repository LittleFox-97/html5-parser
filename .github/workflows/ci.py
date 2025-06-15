#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: Apache 2.0 Copyright: 2017, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shlex
import subprocess
import sys


is_macos = 'darwin' in sys.platform.lower()


def run(*a_str:str) -> None:
    a = shlex.split(a_str[0]) if len(a_str) == 1 else a_str
    ret = subprocess.Popen(a).wait()
    if ret != 0:
        print('Running:', a, 'failed', file=sys.stderr)
        raise SystemExit(ret)


def install_deps():
    if not is_macos:
        run('sudo apt-get update')
        run('sudo apt-get install -y libxml2-dev libxslt-dev')
    deps = 'chardet lxml beautifulsoup4'.split()
    if sys.version_info.major == 2:
        deps.append('BeautifulSoup')
    run(sys.executable, '-m', 'pip', 'install', '--no-binary', 'lxml', *deps)
    run(sys.executable, '-c', 'from lxml import etree; print(etree)')


def main():
    which = sys.argv[-1]
    if hasattr(sys, 'getwindowsversion'):
        run(sys.executable, os.path.join(os.path.dirname(__file__), 'win-ci.py'), which)
        return
    if which == 'install':
        install_deps()
    elif which == 'test':
        builder = os.environ['BUILDER']
        run(sys.executable, builder, 'test')
        if builder == 'unix_build.py':
            run(sys.executable, builder, 'leak')
    else:
        raise SystemExit('Unknown action:', which)


if __name__ == '__main__':
    main()
