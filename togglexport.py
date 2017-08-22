#!/usr/bin/env python
# coding=utf-8

import settings
import requests
import json
from datetime import datetime, timedelta, date
	
def export(date_string):
	if not date_string:
		print("Enter the date you wish to upload in format YYYY-MM-DD. Fallback default is today")
		date_string = raw_input()
	if not date_string:
		mydate = datetime.strftime(date.today(), '%Y-%m-%d')
	else:
		mydate = date_string
	r = requests.get(
		"https://www.toggl.com/api/v8/time_entries",
		params={'start_date': mydate + 'T00:00:00+00:00', 'end_date': mydate + 'T23:59:59+00:00'},
		headers={'Content-Type': 'application/json'},
		auth=(settings.API_TOKEN, 'api_token'),
	)
	return convert(r.text)


def convert(raw_json):
	items = list()
	for raw_item in json.loads(raw_json):
		item = {}
		item[raw_item.get('id')] = {
			'duration': raw_item.get('duration'),
			'contract': get_project_name(raw_item.get('pid')),
			'description': raw_item.get('description'),
			'date': raw_item.get('start').split('T')[0],
		}
		items.append(item)
	return items


def get_project_name(project_id):
	if not project_id:
		return ''
	r = requests.get(
		'https://www.toggl.com/api/v8/projects/' + str(project_id),
		headers={'Content-Type': 'application/json'},
		auth=(settings.API_TOKEN, 'api_token'),
	)
	return json.loads(r.text).get('data').get('name')

