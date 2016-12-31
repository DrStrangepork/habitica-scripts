#!/usr/bin/env python

import argparse, os, requests, time
parser = argparse.ArgumentParser(description="Moves active tasks with duedates to the top of the To-Dos list (excluding todos with future due dates)")


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


headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}

today = unicode(time.strftime("%Y-%m-%d"))
duetoday = []

req = requests.get("https://habitica.com/api/v3/tasks/user?type=todos", headers=headers)

for todo in req.json()['data']:
    # To send only today's todos to the top:    todo['date'][:10] == today:
    # To send all overdue todos to the top:     todo['date'][:10] <= today:
    if 'date' in todo and todo['date'] and todo['date'][:10] <= today:
        duetoday.append(todo)

# Push overdue todos to the top
for todo in sorted(duetoday, key=lambda k: k['date'], reverse=True):
    requests.post("https://habitica.com/api/v3/tasks/" + todo['id'] + "/move/to/0", headers=headers)

# Push today's todos to the top
for todo in [t for t in duetoday if t['date'][:10] == today]:
    requests.post("https://habitica.com/api/v3/tasks/" + todo['id'] + "/move/to/0", headers=headers)
