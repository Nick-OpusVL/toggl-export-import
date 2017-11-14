#!/usr/bin/env python
# coding=utf-8
import mechanize
import settings
import ssl
from datetime import datetime, timedelta
import re
import sys

"""The expected format of data is _currently_
[
    {
        <line_id (anything you wish)>: {
            'duration': <duration of entry in seconds>,
            'date': <date of entry in format YYYY-MM-DD>,
            'description': <entry description>,
            'contract': <exact name of contract>,
        },
    },
    {
        ...
        ...
    },
]
"""

br = mechanize.Browser()

import pprint
def import_data(data):
    prepare_browser()
    login_intranet()
    go_to_timelogger()
    line_dates = set([x.values()[0].get('date') for x in data])
    # Only supporting logging one day entry for now
    if len(line_dates) != 1:
        raise NotImplementedError
    else:
        follow_correct_date_link(next(iter(line_dates)))
        log_lines = {}
        for line in data:
            lv = line.values()[0]
            linekey = (lv['date'], lv['contract'], lv['description'])
            log_lines.setdefault(linekey, []).append(line)

        for ((dt, contract, desc), lines) in log_lines.items():
            log_time_for_group(dt, contract, desc, [l.values()[0] for l in lines])

def log_time_for_line(line):
    follow_log_time_link()
    log_line(line)

def log_time_for_group(dt, contract, description, lines):
    follow_log_time_link()
    total_duration = sum(l['duration'] for l in lines)
    logging_line = {1: {'contract': contract, 'description': description, 'duration': total_duration, 'date': dt}}
    pprint.pprint(logging_line)
    log_line(logging_line)


def log_line(line):
    br.form = list(br.forms())[0]
    project_id_form = br.form.find_control("project_id")
    try:
        project_name = line.values()[0].get('contract')
        if not project_name:
            raise ValueError('No project specified - cannot log this')
        tl_project_id = get_project_id(project_id_form, project_name)
    except ValueError as exc:
        sys.stderr.write("Error: {}\n".format(exc))
        return
    project_id_form.value = [tl_project_id]
    comments_form = br.form.find_control("comments")
    comments_form.value = line.values()[0].get('description')
    days, hours, minutes = get_duration(line.values()[0].get('duration'))
    if days:
        days_form = br.form.find_control("days_spent")
        days_form.value = str(days)
    if hours:
        hours_form = br.form.find_control("hours_spent")
        hours_form.value = str(hours)
    if minutes:
        minutes_form = br.form.find_control("minutes_spent")
        # Round to 15 as the timelogger doesn't support other values
        if not days and not hours and minutes < 15:
            # Always round < 15 up to 15 minutes
            minutes_form.value = "15"
        else:
            minutes_form.value = str(int(15 * round(float(minutes) / 15)))
    import re
    ref = re.match(r'^\[([A-Za-z0-9, ]+)\].*', line.values()[0].get('description', ''))
    if ref:
        br.form.find_control("reference").value = ref.group(1)
    br.submit()

def get_project_id(project_id_form, project_name):
    for item in project_id_form.items:
        if item.get_labels() and item.get_labels()[0].text == project_name:
            return item.name
    raise ValueError("Contract not found in timelogger: {}".format(project_name))

def get_duration(sec):
    d = datetime(1,1,1) + timedelta(seconds=int(sec))
    return d.day-1, d.hour, d.minute

def follow_log_time_link():
    for link in br.links():
        if link.text == 'Log Time':
            br.follow_link(link)

def follow_correct_date_link(date):
    for link in br.links():
        if link.url.endswith(date):
            br.follow_link(link)


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


