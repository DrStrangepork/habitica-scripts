#!/usr/bin/env python3

import argparse
import os
import re
import sys
import requests
from six.moves import range


# MAIN
parser = argparse.ArgumentParser(description="Checks the health of all party members and casts Blessing until all members are above a given threshold")
parser.add_argument('-p', '--hp', '--hitpoints', metavar='[1..49]',
                    type=int, choices=range(1, 50), default=30,
                    help='Minimum HP for all party members (default=30)')
parser.add_argument('-q', '--quiet',
                    action='store_true', default=False,
                    help='quiet (no output)')
parser.add_argument('-v', '--verbose',
                    action='store_true', default=False,
                    help='verbose output')
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

headers = {"x-api-user": args.user_id, "x-api-key": args.api_token, "Content-Type": "application/json"}

req = requests.get(args.baseurl + "groups/party/members", headers=headers, timeout=10)

for member in req.json()['data']:
    mem_req = requests.get(args.baseurl + "members/" + member['id'], headers=headers, timeout=10)
    if args.verbose or (not args.quiet and mem_req.json()['data']['stats']['hp'] < args.hp):
        try:
            print(f"{member['profile']['name']}: {mem_req.json()['data']['stats']['hp']}")
        except UnicodeEncodeError:
            print(f"{member['id']}: {mem_req.json()['data']['stats']['hp']}")
    while mem_req.json()['data']['stats']['hp'] < args.hp:
        os.system("cast-party-spells.py -c blessing -u " + args.user_id + " -k " + args.api_token)
        mem_req = requests.get(args.baseurl + "members/" + member['id'], headers=headers, timeout=10)
        if not args.quiet:
            print(f"{member['profile']['name']}: {mem_req.json()['data']['stats']['hp']}")
