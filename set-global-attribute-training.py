#!/usr/bin/env python

import argparse, json, os, requests, subprocess, sys, time

parser = argparse.ArgumentParser(description="Set the training attribute on your tasks. See http://habitica.wikia.com/wiki/Automatic_Allocation for more info")
parser.add_argument('-a','--attribute', \
                    required=True, \
                    choices=['str','int','con','per'], \
                    help='Attribute to train')
parser.add_argument('-u','--user-id', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('-k','--api-token', \
                    help='From https://habitica.com/#/options/settings/api')
# parser.add_argument('-t','--tag', \
#                     help='Tag of tasks to set (default = all)')
parser.add_argument('--debug', \
                    action='store_true', \
                    help=argparse.SUPPRESS)


# MAIN
if len(sys.argv)==1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()

if args.debug:
    import pdb; pdb.set_trace()

if args.user_id:
    USR = args.user_id
else:
    # Use the environment variable HAB_API_USER,
    # otherwise replace YOUR_USERID_HERE with your User ID
    USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")

if args.api_token:
    KEY = args.api_token
else:
    # Use the environment variable HAB_API_TOKEN,
    # otherwise replace YOUR_KEY_HERE with your API token
    KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

tasksurl = "http://habitica.com/api/v3/tasks/user"
headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}
new_attr = {"attribute":args.attribute}

# Get tasks
req = requests.get(tasksurl, headers=headers)
tasks = req.json()['data']      # List of tasks
# if args.tag:
#     tasks = (x in x where args.tag in task['tags'])

# Update tasks
for task in req.json()['data']:
    taskurl = "https://habitica.com/api/v3/tasks/" + task['id']
    update_req = requests.put(taskurl, headers=headers, data=json.dumps(new_attr))
    # print taskurl, headers, new_attr
    # print update_req.json()
    print task['id']
