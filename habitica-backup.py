#!/usr/bin/env python

import argparse, json, os, requests, sys, time
parser = argparse.ArgumentParser(description="Backs up the JSON data export for offline storage")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
parser.add_argument('-d','--database', \
                    required=True, \
                    help='Path to json db file')
# Set the environment variable HAB_API_USER to your User ID
# or set it via the '-u' argument
parser.add_argument('-u','--user-id', \
                    help='From https://habitica.com/#/options/settings/api')
# Set the environment variable HAB_API_TOKEN to your API token
# or set it via the '-k' argument
parser.add_argument('-k','--api-token', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('--debug', \
                    action=Debug, nargs=0, \
                    help=argparse.SUPPRESS)
if len(sys.argv)==1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()

try:
    if args.user_id is not None:
        USR = args.user_id
    else:
        USR = os.environ['HAB_API_USER']
except KeyError:
    print "Environment variable 'HAB_API_USER' is not set"
    sys.exit(1)

try:
    if args.api_token is not None:
        KEY = args.api_token
    else:
        KEY = os.environ['HAB_API_TOKEN']
except KeyError:
    print "Environment variable 'HAB_API_TOKEN' is not set"
    sys.exit(1)


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
