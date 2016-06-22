#!/usr/bin/python3
from __future__ import print_function

import os
import subprocess
import itertools
import atexit
import time
import argparse

DEFAULT = '\x1b[0m'
BOLD = '\x1b[1m'
REVERSE = '\x1b[7m'
CLEAR = "\x1b[1;1H\x1b[2J"

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--pid', type=int, default=os.getppid())
parser.add_argument('directory', nargs='*', default=('.'))

def dolist(directory, level=0, number=1, special=None, maxfiles=3):
    found = REVERSE if os.path.realpath(directory) == special else ''
    if (number > maxfiles - 1 and not found and
        not special.startswith(os.path.realpath(directory))):
        return None
    if level == 0:
        dirname = os.path.realpath(directory)
    else:
        dirname = os.path.basename(directory)
    print(found + level * '    ' + BOLD + dirname + DEFAULT + found + os.sep,
          end='\n' + DEFAULT)
    items = [directory + os.path.sep + item
             for item in os.listdir(directory)]
    prevans = False
    prefix = (level + 1) * '    '
    for num, dir in enumerate(filter(os.path.isdir, items)):
        ans = dolist(dir, level + 1, num, special)
        found = found if found else ans if ans is not None else found
        if ans is None and prevans == False:
            print(prefix + '...' + dir)
        prevans = ans
        if num > maxfiles + 1 and found:
            break
    for num, file in enumerate(itertools.filterfalse(os.path.isdir, items)):
        if num > maxfiles:
            print(prefix + '...')
            break
        else:
            print(prefix + os.path.basename(file))
    return found

def create_watch(directories, pid):
    cmd = 'inotifywait -m -q -e create -e delete -e move -r'.split()
    c = subprocess.Popen(cmd + list(directories),
                         stdout=subprocess.PIPE)
    if pid:
        cmd2 = 'strace -e chdir -qq -e signal= -o /dev/stdout -p'.split()
        c2 = subprocess.Popen(cmd2 + [str(pid)],
                              stdout=c.stdout)
    atexit.register(lambda: c.terminate())
    atexit.register(lambda: c2.terminate())
    return c.stdout

def wait_watch(input, at_least=1):
    start = time.time()
    while time.time() < start + at_least:
        input.readline()

def main(directories, pid):
    watch = create_watch(directories, pid)
    cwd = '/proc/{}/cwd'.format(pid)
    while True:
        print(end=CLEAR)
        special = os.readlink(cwd)
        for dir in directories:
            dolist(dir, special=special)
        wait_watch(watch)

if __name__ == '__main__':
    opts = parser.parse_args()
    main(opts.directory, opts.pid)
