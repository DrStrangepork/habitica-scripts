#!/usr/bin/env python2

import argparse, os, requests, sys
parser = argparse.ArgumentParser(\
                description="Checks the health of all party members and casts \
                Blessing until all members are above a given threshold")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
parser.add_argument('-p', '--hp', '--hitpoints',metavar='[1..49]',
                    type=int, choices=xrange(1, 50), default=30,
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

req = requests.get(args.baseurl + "groups/party/members", headers=headers)

for member in req.json()['data']:
    mem_req = requests.get(args.baseurl + "members/" + member['id'], headers=headers)
    if args.verbose or (not args.quiet and mem_req.json()['data']['stats']['hp'] < args.hp):
        try:
            print "{}: {}".format(member['profile']['name'], mem_req.json()['data']['stats']['hp'])
        except UnicodeEncodeError:
            print "{}: {}".format(member['id'], mem_req.json()['data']['stats']['hp'])
    while mem_req.json()['data']['stats']['hp'] < args.hp:
        os.system("cast-party-spells.py -c blessing -u " + args.user_id + " -k " + args.api_token)
        mem_req = requests.get(args.baseurl + "members/" + member['id'], headers=headers)
        if not args.quiet:
            print "{}: {}".format(member['profile']['name'], mem_req.json()['data']['stats']['hp'])
