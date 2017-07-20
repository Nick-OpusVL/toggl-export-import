#!/usr/bin/env python
# coding=utf-8

import settings
import requests
import pdb
import json
from datetime import datetime, timedelta, date
	
def export():
	print("Enter the start date in format YYYY-MM-DD")
	start_string = raw_input()
	# Set a suitable default fallback of yesterday
	if not start_string:
		# TODO:
		pass
	else:
		start_date = datetime.strptime(start_string, '%Y-%m-%d').isoformat() + '+01:00'
	print("Enter the end date in format YYYY-MM-DD")
	end_date = datetime.strptime(raw_input(), '%Y-%m-%d').isoformat() + '+01:00'
	r = requests.get(
		"https://www.toggl.com/api/v8/time_entries",
		params={'start_date': start_date, 'end_date': end_date},
		headers={'Content-Type': 'application/json'},
		auth=(settings.API_TOKEN, 'api_token'),
	)
	converted_data = convert(r.text)
	for item in converted_data:
		for k, v in item.items():
			print k, v


def convert(raw_json):
	items = list()
	for raw_item in json.loads(raw_json):
		item = {}
		item[raw_item.get('id')] = {
			'duration': raw_item.get('duration'),
			'contract': get_project_name(raw_item.get('pid')),
			# No client id given by api :(
			# 'contract': get_client_name(raw_item.get('cid')),
			'description': raw_item.get('description'),
		}
		items.append(item)
	return items

# def get_client_name(client_id):
# 	if not client_id:
# 		return ''
# 	r = requests.get(
# 		'https://www.toggl.com/api/v8/clients/' + str(client_id),
# 		headers={'Content-Type': 'application/json'},
# 		auth=(settings.API_TOKEN, 'api_token'),
# 	)
# 	return json.loads(r.text).get('data').get('name')

def get_project_name(project_id):
	if not project_id:
		return ''
	r = requests.get(
		'https://www.toggl.com/api/v8/projects/' + str(project_id),
		headers={'Content-Type': 'application/json'},
		auth=(settings.API_TOKEN, 'api_token'),
	)
	return json.loads(r.text).get('data').get('name')

export()