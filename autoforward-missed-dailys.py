#!/usr/bin/env python

import argparse, json, os, requests, sys, time
parser = argparse.ArgumentParser(description="Add missed dailys to the current day's dailys")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
parser.add_argument('-t','--tag',
                    type=str, default="auto-forward",
                    help='Auto-forward tag')
parser.add_argument('-m','--message',
                    type=str, default="AUTO-FORWARDED",
                    help='Reminder message added to task title')
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

# Get auto-forward tag id
req = requests.get(args.baseurl + "tags", headers=headers)
for tag in (x for x in req.json()['data'] if x['name'] == args.tag):
    TAGID = tag['id']

# Abort if auto-forward tag not found
try:
    TAGID
except NameError:
    print "Auto-forward tag '{}' not found".format(args.tag)
    sys.exit(1)

# Abort if you are resting at the inn
req = requests.get(args.baseurl + "user", headers=headers)
if req.json()['data']['preferences']['sleep']:
    print "Resting in the Inn, auto-forwarding cancelled"
    sys.exit()

days = ("su", "m", "t", "w", "th", "f", "s")
# day of week (0..6); 0 is Sunday
daynum = int(time.strftime("%w"))
today = days[daynum]
yesterday = days[daynum-1]

req = requests.get(args.baseurl + "tasks/user?type=dailys", headers=headers)

for daily in (x for x in req.json()['data'] if TAGID in x['tags']):
    if daily['repeat'][yesterday] and daily['streak'] == 0:
        daily['repeat'][today] = True
        daily['text'] += " {}".format(args.message)
        task = requests.put(args.baseurl + "tasks/" + daily['id'], headers=headers, data=json.dumps(daily))
