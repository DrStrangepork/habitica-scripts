#!/usr/bin/env python2

import argparse
import json
import os
import requests
import sys


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
parser = argparse.ArgumentParser(description="Dumps your user data to a file user-data.json in the current directory")
parser.add_argument('-o', '--outfile',
                    type=argparse.FileType('w'), default="user-data.json",
                    help='JSON data file (default: user-data.json)')
parser.add_argument('-u', '--user-id',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_USER')
parser.add_argument('-k', '--api-token',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_TOKEN')
parser.add_argument('--baseurl',
                    type=str, default="https://habitica.com",
                    help='API server (default: https://habitica.com)')
parser.add_argument('--debug',
                    action=Debug, nargs=0,
                    help=argparse.SUPPRESS)
args = parser.parse_args()
args.baseurl += "/api/v3/"

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

req = requests.get(args.baseurl + "user", headers=headers)
# with open(args.outfile, 'w') as f:
json.dump(req.json(),args.outfile,separators=(',',':'),sort_keys=True)
