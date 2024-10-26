#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
import time
import requests


# MAIN
parser = argparse.ArgumentParser(description="Add missed dailys to the current day's dailys")
parser.add_argument('-t', '--tag',
                    type=str, default="auto-forward",
                    help='Auto-forward tag')
parser.add_argument('-m', '--message',
                    type=str, default="AUTO-FORWARDED",
                    help='Reminder message added to task title')
parser.add_argument('-u', '--user-id',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_USER')
parser.add_argument('-k', '--api-token',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_TOKEN')
parser.add_argument('-v', '--verbose',
                    action='store_true', default=False,
                    help='Verbose output')
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


headers = {"x-api-user": args.user_id, "x-api-key": args.api_token, "Content-Type": "application/json"}

# Get auto-forward tag id
req = requests.get(args.baseurl + "tags", headers=headers, timeout=10)
if req.reason == 'Not Found':
    print("You have no tags")
    sys.exit(0)
tag = [x for x in req.json()['data'] if x.get('name', None) == args.tag]
if not tag:
    print(f"Auto-forward tag '{args.tag}' not found")
    sys.exit(1)
tag_id = tag[0]['id']
if args.verbose: print(f'tag: {tag[0]}')

# Abort if you are resting at the inn
req = requests.get(args.baseurl + "user", headers=headers, timeout=10)
if req.json()['data']['preferences']['sleep']:
    print("Resting in the Inn, auto-forwarding cancelled")
    sys.exit()

days = ("su", "m", "t", "w", "th", "f", "s")
# day of week (0..6); 0 is Sunday
daynum = int(time.strftime("%w"))
today = days[daynum]
yesterday = days[daynum - 1]

req = requests.get(args.baseurl + "tasks/user?type=dailys", headers=headers, timeout=10)
if req.reason == 'Not Found':
    print("You have no Dailys")
    sys.exit(0)

dailys_to_forward = [x for x in req.json()['data'] if tag_id in x['tags'] and x['repeat'][yesterday] and x['streak'] == 0 and not x['repeat'][today]]
if not dailys_to_forward and args.verbose:
    print("No dailys to forward")
    sys.exit()

for daily in dailys_to_forward:
    if args.verbose: print(f"Forwarding daily \"{daily['text']}\"")
    daily['repeat'][today] = True
    daily['text'] += f' {args.message}'
    task = requests.put(args.baseurl + "tasks/" + daily['id'], headers=headers, timeout=10, data=json.dumps(daily))
