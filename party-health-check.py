#!/usr/bin/env python

import argparse, os, requests, sys
parser = argparse.ArgumentParser(\
                description="Checks the health of all party members and casts \
                Blessing until all members are above a given threshold")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
parser.add_argument('-p','--hp','--hitpoints',metavar='[1..49]', \
                    type=int, choices=xrange(1, 50), default=30,
                    help='Minimum HP for all party members (default=30)')
parser.add_argument('-q','--quiet', \
                    action='store_true', default=False, \
                    help='quiet (no output)')
parser.add_argument('-v','--verbose', \
                    action='store_true', default=False, \
                    help='verbose output')
# Set the environment variable HAB_API_USER to your User ID
# or set it via the '-u' argument
parser.add_argument('-u','--user-id', \
                    help='From https://habitica.com/#/options/settings/api')
# Set the environment variable HAB_API_TOKEN to your API token
# or set it via the '-k' argument
parser.add_argument('-k','--api-token', \
                    help='From https://habitica.com/#/options/settings/api')
# Set the Habitica URL (useful for testing local install)
parser.add_argument('--baseurl', \
                    help=argparse.SUPPRESS)
parser.add_argument('--debug', \
                    action=Debug, nargs=0, \
                    help=argparse.SUPPRESS)
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

if args.baseurl is not None:
    URL = args.baseurl + "/api/v3/"
else:
    URL = "https://habitica.com/api/v3/"


headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}

req = requests.get(URL + "groups/party/members", headers=headers)

for member in req.json()['data']:
    mem_req = requests.get(URL + "members/" + member['id'], headers=headers)
    if args.verbose or (not args.quiet and mem_req.json()['data']['stats']['hp'] < args.hp):
        print "{}: {}".format(member['profile']['name'], mem_req.json()['data']['stats']['hp'])
    while mem_req.json()['data']['stats']['hp'] < args.hp:
        os.system("cast-party-spells.py -c blessing -u " + USR + " -k " + KEY)
        mem_req = requests.get(URL + "members/" + member['id'], headers=headers)
        if not args.quiet:
            print "{}: {}".format(member['profile']['name'], mem_req.json()['data']['stats']['hp'])
