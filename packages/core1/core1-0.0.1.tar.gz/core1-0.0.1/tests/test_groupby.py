#!/usr/bin/env python

def test_groupby():

    import os
    import textwrap

    desired = textwrap.dedent("""
    9591818c07e900db7e1e0bc4b884c945e6a61b24	tests/data/2.txt	tests/data/4.txt
    f572d396fae9206628714fb2ce00f72e94f2258f	tests/data/1.txt	tests/data/3.txt
    """).strip()

    output = os.popen("""
        find tests/data/ -type f | xargs sha1sum | groupby
    """).read().strip()

    assert output == desired
