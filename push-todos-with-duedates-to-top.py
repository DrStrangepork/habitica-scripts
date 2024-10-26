#!/usr/bin/env python3

import argparse
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests
import six


def convert_to_local_time(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc_time = utc_time.replace(tzinfo=timezone.utc)
    local_time = utc_time.astimezone(local_tz)
    return local_time.strftime("%Y-%m-%d")


# MAIN
local_tz = datetime.now().astimezone().tzinfo  # Auto-detect local timezone
parser = argparse.ArgumentParser(
    description="Moves active tasks with duedates to the top of the To-Dos list in order of duedate")
group = parser.add_mutually_exclusive_group()
group.add_argument('-t', '--today',
                action='store_true', default=False,
                help='send only today\'s todos to the top')
parser.add_argument('-f', '--future',
                    action='store_true', default=False,
                    help='include todos with future due dates')
parser.add_argument('-v', '--verbose',
                    action='store_true', default=False,
                    help='show which todos are being moved')
parser.add_argument('-u', '--user-id',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_USER')
parser.add_argument('-k', '--api-token',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_TOKEN')
parser.add_argument('--baseurl',
                    type=str, default="https://habitica.com",
                    help='API server (default: https://habitica.com)')
args = parser.parse_args()
args.baseurl += "/api/v3/"

try:
    if args.user_id is None:
        args.user_id = os.environ['HAB_API_USER']
    if not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', args.user_id, re.IGNORECASE):
        print(f"Invalid User ID: '{args.user_id}'")
        sys.exit(1)
except KeyError:
    print("User ID must be set by the -u/--user-id option or by setting the environment variable 'HAB_API_USER'")
    sys.exit(1)

try:
    if args.api_token is None:
        args.api_token = os.environ['HAB_API_TOKEN']
    if not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', args.api_token, re.IGNORECASE):
        print(f"Invalid API Token: '{args.api_token}'")
        sys.exit(1)
except KeyError:
    print("API Token must be set by the -k/--api-token option or by setting the environment variable 'HAB_API_TOKEN'")
    sys.exit(1)


headers = {"x-api-user": args.user_id, "x-api-key": args.api_token,
           "Content-Type": "application/json"}

today = six.text_type(time.strftime("%Y-%m-%d"))
todos_with_duedates = []

req = requests.get(args.baseurl + "tasks/user?type=todos", headers=headers, timeout=10)
if req.reason == 'Not Found':
    print("You have no To-Dos")
    sys.exit(0)

for todo in [t for t in req.json()['data'] if ('date' in t and t['date'])]:
    todo['local_date'] = convert_to_local_time(todo['date'])
    if ((args.future and todo['local_date'] > today)     # pylint: disable=too-many-boolean-expressions
            or (args.today and todo['local_date'] == today)
            or (not args.today and todo['local_date'] <= today)):
        todos_with_duedates.append(todo)
        if args.verbose: print(todo['text'])
todos_with_duedates.sort(key=lambda k: (k['local_date'], k['value']), reverse=True)

# Push todos_with_duedates to the top
for todo in todos_with_duedates:
    requests.post(args.baseurl + f"tasks/{todo['id']}/move/to/0", headers=headers, timeout=10)
