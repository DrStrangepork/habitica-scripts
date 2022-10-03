#!/usr/bin/env python3

import argparse
import os
import time
import sys
import requests
import six


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb
        pdb.set_trace()


# MAIN
parser = argparse.ArgumentParser(
    description="Moves active tasks with duedates to the top of the To-Dos list in order of duedate")
group = parser.add_mutually_exclusive_group()
group.add_argument('-t', '--today',
                   action='store_true', default=False,
                   help='send only today\'s todos to the top')
parser.add_argument('-f', '--future',
                    action='store_true', default=False,
                    help='include todos with future due dates')
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
    print("User ID must be set by the -u/--user-id option or by setting the environment variable 'HAB_API_USER'")
    sys.exit(1)

try:
    if args.api_token is None:
        args.api_token = os.environ['HAB_API_TOKEN']
except KeyError:
    print("API Token must be set by the -k/--api-token option or by setting the environment variable 'HAB_API_TOKEN'")
    sys.exit(1)


headers = {"x-api-user": args.user_id, "x-api-key": args.api_token,
           "Content-Type": "application/json"}

today = six.text_type(time.strftime("%Y-%m-%d"))
todos_with_duedates = []

req = requests.get(args.baseurl + "tasks/user?type=todos", headers=headers)

for todo in [t for t in req.json()['data'] if ('date' in t and t['date'])]:
    if ((args.future and todo['date'][:10] > today)
            or (args.today and todo['date'][:10] == today)
            or (not args.today and todo['date'][:10] <= today)):
        todos_with_duedates.append(todo)
todos_with_duedates.sort(key=lambda k: (k['date'][:10], k['createdAt']), reverse=True)

# Push todos_with_duedates to the top
for todo in todos_with_duedates:
    requests.post(args.baseurl + "tasks/"
                  + todo['id'] + "/move/to/0", headers=headers)
