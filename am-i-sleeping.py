#!/usr/bin/env python

import argparse, os, requests
parser = argparse.ArgumentParser(description="Organize your tasks with emoji priority emoticons",
            epilog='''This method of task prioritization and organization is loosely based
                on the Franklin-Covey ABC model which is similar to the Horizons of Focus
                model in a GTD (Getting Things Done) methodology. For more information on
                GTD with Habitica, see http://habitica.wikia.com/wiki/GTD_with_Habitica''')


# MAIN
# Use the environment variable HAB_API_USER,
# otherwise replace YOUR_USERID_HERE with your User ID
USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
# Use the environment variable HAB_API_TOKEN,
# otherwise replace YOUR_KEY_HERE with your API token
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

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

# MAIN
req = requests.get("https://habitica.com/api/v3/user", headers=headers)
if req.json()['data']['preferences']['sleep']:
    print "Yes"
else:
    print "No"
