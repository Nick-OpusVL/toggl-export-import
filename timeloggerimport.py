#!/usr/bin/env python
# coding=utf-8
import mechanize
import settings
import ssl

br = mechanize.Browser()

def import_data(data):
    prepare_browser()
    login_intranet()
    go_to_timelogger()
    for line in data:
        fill_out_timelogger(line)

def fill_out_timelogger(line):
    pass

def go_to_timelogger():
    for link in br.links():
        if link.url == 'https://opusvl-intranet/modules/timelogger/entries':
            br.follow_link(link)

def prepare_browser():
    # Get pas HTTP Error 403
    br.set_handle_robots(False)
    # Get past SSL verification
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

def login_intranet():
    br.open("https://opusvl-intranet/login")
    # Timelogger form has no name
    br.form = list(br.forms())[0]
    username_field = br.form.find_control("username")
    username_field.value = settings.TL_USERNAME
    password_field = br.form.find_control("password")
    password_field.value = settings.TL_PASSWORD
    br.submit()


