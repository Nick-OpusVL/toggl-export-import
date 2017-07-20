#!/usr/bin/env python
# coding=utf-8

import togglexport
import timeloggerimport

def run():
    timeloggerimport.import_data(togglexport.export())

run()
