#!/usr/bin/env python3

"""
    shell groupby
"""

def main(argv=None):

    import os
    import io
    import sys
    import argparse

    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', type=str, default=None, help="File to process")
    parser.add_argument('-f', '--field', type=int, default=1, help="Column number to group by")
    parser.add_argument('-F', '--in-sep', type=str, default='\s+', help="Input field separator")
    parser.add_argument('-1', '--out-sep-1', type=str, default='\t', help="Output index separator")
    parser.add_argument('-2', '--out-sep-2', type=str, default='\t', help="Output field separator")
    args = parser.parse_args(argv)

    if args.file is None:
        file = io.StringIO(sys.stdin.read())
    else:
        file = args.file

    import signalhandlers
    signalhandlers.install_exit_on_sigpipe_handler()

    import pandas as pd
    df = pd.read_csv(file, sep=args.in_sep, header=None)
    df.columns = list(range(1, len(df.columns)+1))
    groups = df.groupby(args.field)

    colon = args.out_sep_1
    comma = args.out_sep_2

    for key, group in groups:
        g = group.set_index(args.field)
        v = g.values.ravel()
        fmt = comma.join(map(str, v))
        line = f"{key}{colon}{fmt}"
        print(line)

if __name__ == '__main__':
    main(sys.argv[1:])
