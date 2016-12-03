#!/usr/bin/env python

import argparse, os, requests, time
parser = argparse.ArgumentParser(description="Moves active tasks with duedates to the top of the To-Dos list (excluding todos with future due dates)")


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

# parser.add_argument('-t','--due-today', \
#                     action=store_boolean, nargs=0, \
#                     help='Push only today\'s todos to the top')
# parser.add_argument('-o','--overdue', \
#                     action=store_boolean, nargs=0, \
#                     help='Push only overdue todos to the top')
# parser.add_argument('-a','--all', \
#                     action=store_boolean, nargs=0, \
#                     help='Push all todos to the top')
# parser.add_argument('-r','--reverse', \
#                     action=store_boolean, nargs=0, \
#                     help='Sort overdue tasks ')
parser.add_argument('-u','--user-id', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('-k','--api-token', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('--debug', \
                    action=Debug, nargs=0, \
                    help=argparse.SUPPRESS)
args = parser.parse_args()

if args.user_id is not None:
    USR = args.user_id

if args.api_token is not None:
    KEY = args.api_token

headers = {"x-api-user":USR,"x-api-key":KEY,"Content-Type":"application/json"}

duedate = unicode(time.strftime("%Y-%m-%d"))
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
