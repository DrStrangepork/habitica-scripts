#!/usr/bin/env python

import argparse, json, os, requests, sys, time
parser = argparse.ArgumentParser(description="Set the training attribute on your tasks",
            epilog="For more info on attribute training, see http://habitica.wikia.com/wiki/Automatic_Allocation")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
# Use the environment variable HAB_API_USER,
# otherwise replace YOUR_USERID_HERE with your User ID
USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
# Use the environment variable HAB_API_TOKEN,
# otherwise replace YOUR_KEY_HERE with your API token
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

parser.add_argument('-d','--database', \
                    required=True, \
                    help='Path to json db file')
parser.add_argument('-u','--user-id', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('-k','--api-token', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('--debug', \
                    action=Debug, nargs=0, \
                    help=argparse.SUPPRESS)
if len(sys.argv)==1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()

if args.user_id is not None:
    USR = args.user_id

if args.api_token is not None:
    KEY = args.api_token

headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}
now = unicode(time.strftime("%Y-%m-%dT%H:%M:%S%z"))

# Load DB
if not os.path.isfile(args.database):
    with open(args.database, 'w') as f:
        f.write("[]")
    f.close
with open(args.database, 'r') as f:
    DB = json.load(f)

# Get profile
req = requests.get("https://habitica.com/export/userdata.json", headers=headers)

# Add profile
new = {}
new[now] = req.json()
DB.append(new)

# Save DB
with open(args.database, 'w') as f:
    json.dump(DB,f,separators=(',',':'),sort_keys=True)
