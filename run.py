#!/usr/bin/env python
# coding=utf-8
import sys
import togglexport
import timeloggerimport

def run():
    """
    Usage:
        $ python run.py 2017-08-20
        OR
        $ python run.py
        <input date on prompt>
        OR
        $ python run.py
        <input no date - fallback is today>
    """
    date = False
    if len(sys.argv) > 1:
        date = sys.argv[1]
    timeloggerimport.import_data(togglexport.export(date))

run()
