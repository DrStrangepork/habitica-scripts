#!/usr/bin/env python

import argparse, json, os, requests, sys, time
parser = argparse.ArgumentParser(description="Backs up the JSON data export for offline storage")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
parser.add_argument('-d','--database',
                    required=True,
                    help='Path to json db file')
parser.add_argument('-u','--user-id',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_USER')
parser.add_argument('-k','--api-token',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_TOKEN')
parser.add_argument('--baseurl',
                    type=str, default="https://habitica.com",
                    help='API server (default: https://habitica.com)')
parser.add_argument('--debug',
                    action=Debug, nargs=0,
                    help=argparse.SUPPRESS)
if len(sys.argv)==1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()

try:
    if args.user_id is None:
        args.user_id = os.environ['HAB_API_USER']
except KeyError:
    print "User ID must be set by the -u/--user-id option or by setting the environment variable 'HAB_API_USER'"
    sys.exit(1)

try:
    if args.api_token is None:
        args.api_token = os.environ['HAB_API_TOKEN']
except KeyError:
    print "API Token must be set by the -k/--api-token option or by setting the environment variable 'HAB_API_TOKEN'"
    sys.exit(1)


headers = {"x-api-user":args.user_id,"x-api-key":args.api_token,"Content-Type":"application/json"}
now = unicode(time.strftime("%Y-%m-%dT%H:%M:%S%z"))

# Load DB
if not os.path.isfile(args.database):
    with open(args.database, 'w') as f:
        f.write("[]")
    f.close
with open(args.database, 'r') as f:
    DB = json.load(f)

# Get profile
req = requests.get(args.baseurl + "/export/userdata.json", headers=headers)

# Add profile
new = {}
new[now] = req.json()
DB.append(new)

# Save DB
with open(args.database, 'w') as f:
    json.dump(DB,f,separators=(',',':'),sort_keys=True)
