#!/usr/bin/env python

import argparse, json, os, requests, sys, time
parser = argparse.ArgumentParser(description="Add missed dailys to the current day's dailys")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
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


TAG = "auto-forward"
TXT = "AUTO-FORWARDED"
headers = {"x-api-user":USR,"x-api-key":KEY,"Content-Type":"application/json"}

# Get autoforward tag id
tagsurl = "https://habitica.com/api/v3/tags"
req = requests.get(tagsurl, headers=headers)
for tag in (x for x in req.json()['data'] if x['name'] == TAG):
    TAGID = tag['id']

# Abort if autoforward tag not found
try:
    TAGID
except NameError:
    # print "Autoforward tag \"{}\" not found".format(TAG)
    quit()

# Abort if you are resting at the inn
userurl = "https://habitica.com/api/v3/user"
req = requests.get(userurl, headers=headers)
if req.json()['data']['preferences']['sleep']:
    # print "Resting in the Inn, autoforwarding cancelled"
    quit()

days = ("su", "m", "t", "w", "th", "f", "s")
# day of week (0..6); 0 is Sunday
daynum = int(time.strftime("%w"))
today = days[daynum]
yesterday = days[daynum-1]

# Get dailys
tasksurl = "https://habitica.com/api/v3/tasks/user?type=dailys"
req = requests.get(tasksurl, headers=headers)

for daily in (x for x in req.json()['data'] if TAGID in x['tags']):
    if daily['repeat'][yesterday] and daily['streak'] == 0:
        daily['repeat'][today] = True
        daily['text'] += " {}".format(TXT)
        taskurl = "https://habitica.com/api/v3/tasks/" + daily['id']
        task = requests.put(taskurl, headers=headers, data=json.dumps(daily))
