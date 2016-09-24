#!/usr/bin/env python

import argparse, json, os, requests, sys
parser = argparse.ArgumentParser(description="Set the training attribute on your tasks",
            epilog="For more info on attribute training, see http://habitica.wikia.com/wiki/Automatic_Allocation")


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

parser.add_argument('-a','--attribute', \
                    required=True, \
                    choices=['str','int','con','per'], \
                    help='Attribute to train')
parser.add_argument('-u','--user-id', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('-k','--api-token', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('--debug', \
                    action=Debug, nargs=0, \
                    help=argparse.SUPPRESS)
if len(sys.argv)==1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()

if args.user_id is not None:
    USR = args.user_id

if args.api_token is not None:
    KEY = args.api_token

headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}
new_attr = {"attribute":args.attribute}

# Get tasks
req = requests.get("http://habitica.com/api/v3/tasks/user", headers=headers)
tasks = req.json()['data']      # List of tasks

# Update tasks
for task in req.json()['data']:
    taskurl = "https://habitica.com/api/v3/tasks/" + task['id']
    update_req = requests.put(taskurl, headers=headers, data=json.dumps(new_attr))
