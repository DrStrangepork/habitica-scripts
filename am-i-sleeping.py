#!/usr/bin/env python

import argparse, os, requests, sys
parser = argparse.ArgumentParser(description="Are you sleeping at the Inn? Returns \"Yes\" or \"No\"")


# MAIN
# Use the environment variable HAB_API_USER,
# otherwise replace YOUR_USERID_HERE with your User ID
USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
# Use the environment variable HAB_API_TOKEN,
# otherwise replace YOUR_KEY_HERE with your API token
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

parser.add_argument('-e','--error-code', \
                    action='store_true', \
                    help='Returns 0 or 1 rather than "Yes" of "No"')
parser.add_argument('-u','--user-id', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('-k','--api-token', \
                    help='From https://habitica.com/#/options/settings/api')
args = parser.parse_args()

if args.user_id is not None:
    USR = args.user_id

if args.api_token is not None:
    KEY = args.api_token

headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}

req = requests.get("https://habitica.com/api/v3/user", headers=headers)
if req.json()['data']['preferences']['sleep']:
    if args.error_code:
        sys.exit(0)
    else:
        print "Yes"
else:
    if args.error_code:
        sys.exit(1)
    else:
        print "No"
