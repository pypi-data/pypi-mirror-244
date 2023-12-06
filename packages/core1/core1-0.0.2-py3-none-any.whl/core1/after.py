#!/usr/bin/env python

def main(argv=None):

    import os
    import re
    import sys
    import argparse

    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog='after',
        description='Print lines after first match of pattern',
    )
    parser.add_argument('regex')
    parser.add_argument('-i', '--inclusive', action='store_true')
    args = parser.parse_args(argv)

    import signalhandlers
    signalhandlers.install_exit_on_sigpipe_handler()

    for line in sys.stdin:
        if re.search(args.regex, line):
            break

    if args.inclusive:
        sys.stdout.write(line)

    for line in sys.stdin:
        sys.stdout.write(line)

if __name__ == '__main__':
    main(sys.argv[1:])
