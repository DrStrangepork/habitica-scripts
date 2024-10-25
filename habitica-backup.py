#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
import time
import requests
import six


# MAIN
parser = argparse.ArgumentParser(description="Backs up the JSON data export for offline storage")
parser.add_argument('-d', '--database',
                    type=argparse.FileType('w'), default="habitica-data.json",
                    help='JSON data file (default: habitica-data.json)')
parser.add_argument('-u', '--user-id',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_USER')
parser.add_argument('-k', '--api-token',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_TOKEN')
parser.add_argument('--baseurl',
                    type=str, default="https://habitica.com",
                    help='API server (default: https://habitica.com)')
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()

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
now = six.text_type(time.strftime("%Y-%m-%dT%H:%M:%S%z"))

# Load DB
if not os.path.isfile(args.database):
    with open(args.database, 'w', encoding='utf-8') as f:
        f.write("[]")
with open(args.database, 'r', encoding='utf-8') as f:
    DB = json.load(f)

# Get profile
req = requests.get(args.baseurl + "/export/userdata.json", headers=headers)

# Add profile
new = {}
new[now] = req.json()
DB.append(new)

# Save DB
with open(args.database, 'w', encoding='utf-8') as f:
    json.dump(DB, f, separators=(',', ':'), sort_keys=True)
