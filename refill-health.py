#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
import requests


# MAIN
parser = argparse.ArgumentParser(description="Increases health points if less than given threshold")
parser.add_argument('-p', '--hp', '--healthpoints',
                    type=int, default=30,
                    help='Minimum HP (default=10)')
parser.add_argument('-m', '--multiplier',
                    type=int, default=5,
                    help='Multiplier (default=5)')
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
args.baseurl += "/api/v3/user"

if args.hp <= 0 or args.multiplier <= 0:
    print("Value must be a positive number")
    sys.exit(1)

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

req = requests.get(args.baseurl, headers=headers, timeout=10)

if req.json()['data']['stats']['hp'] < args.hp:
    data = {}
    data['stats.hp'] = req.json()['data']['stats']['hp'] * args.multiplier
    stat = requests.put(args.baseurl, headers=headers, timeout=10, data=json.dumps(data))
