#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
import time
from operator import itemgetter
import requests


# MAIN
parser = argparse.ArgumentParser(description="A 30-day escalating ab/squat exercise routine")
parser.add_argument('-u', '--user-id',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_USER')
parser.add_argument('-k', '--api-token',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_TOKEN')
parser.add_argument('--baseurl',
                    type=str, default="https://habitica.com",
                    help='API server (default: https://habitica.com)')
args = parser.parse_args()
args.baseurl += "/api/v3/"

try:
    if args.user_id is None:
        args.user_id = os.environ['HAB_API_USER']
    if not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', args.user_id, re.IGNORECASE):
        print(f"Invalid User ID: '{args.user_id}'")
        sys.exit(1)
except KeyError:
    print("User ID must be set by the -u/--user-id option or by setting the environment variable 'HAB_API_USER'")
    sys.exit(1)

try:
    if args.api_token is None:
        args.api_token = os.environ['HAB_API_TOKEN']
    if not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', args.api_token, re.IGNORECASE):
        print(f"Invalid API Token: '{args.api_token}'")
        sys.exit(1)
except KeyError:
    print("API Token must be set by the -k/--api-token option or by setting the environment variable 'HAB_API_TOKEN'")
    sys.exit(1)


headers = {"x-api-user": args.user_id, "x-api-key": args.api_token, "Content-Type": "application/json"}
schedule = [
    {"day": "01", "notes": "Crunches 10\nSit-ups 10\nSquats 25"}, {"day": "02", "notes": "Crunches 15\nSit-ups 20\nSquats 30"},
    {"day": "03", "notes": "Crunches 20\nSit-ups 5\nSquats 35"},  {"day": "04", "notes": "Crunches 25\nSit-ups 10\nSquats 40"},
    {"day": "05", "notes": "Crunches 10\nSit-ups 5\nSquats 30"},  {"day": "06", "notes": "Crunches 30\nSit-ups 15\nSquats 50"},
    {"day": "07", "notes": "Crunches 35\nSit-ups 20\nSquats 55"}, {"day": "08", "notes": "Crunches 40\nSit-ups 30\nSquats 60"},
    {"day": "09", "notes": "Rest Day"},                           {"day": "10", "notes": "Crunches 10\nSit-ups 10\nSquats 25"},
    {"day": "11", "notes": "Crunches 50\nSit-ups 40\nSquats 65"}, {"day": "12", "notes": "Crunches 60\nSit-ups 45\nSquats 70"},
    {"day": "13", "notes": "Crunches 5\nSit-ups 5\nSquats 5"},    {"day": "14", "notes": "Crunches 10\nSit-ups 10\nSquats 10"},
    {"day": "15", "notes": "Crunches 30\nSit-ups 20\nSquats 20"}, {"day": "16", "notes": "Crunches 30\nSit-ups 25\nSquats 45"},
    {"day": "17", "notes": "Crunches 50\nSit-ups 40\nSquats 60"}, {"day": "18", "notes": "Rest Day"},
    {"day": "19", "notes": "Crunches 5\nSit-ups 5\nSquats 5"},    {"day": "20", "notes": "Crunches 10\nSit-ups 10\nSquats 25"},
    {"day": "21", "notes": "Crunches 15\nSit-ups 20\nSquats 35"}, {"day": "22", "notes": "Crunches 25\nSit-ups 20\nSquats 55"},
    {"day": "23", "notes": "Crunches 40\nSit-ups 10\nSquats 55"}, {"day": "24", "notes": "Crunches 50\nSit-ups 10\nSquats 65"},
    {"day": "25", "notes": "Crunches 60\nSit-ups 15\nSquats 65"}, {"day": "26", "notes": "Crunches 70\nSit-ups 20\nSquats 85"},
    {"day": "27", "notes": "Rest Day"},                           {"day": "28", "notes": "Crunches 80\nSit-ups 25\nSquats 95"},
    {"day": "29", "notes": "Crunches 90\nSit-ups 30\nSquats 95"}, {"day": "30", "notes": "Crunches 40\nSit-ups 40\nSquats 100"}
]

req = requests.post(args.baseurl + "tasks/user", headers=headers, json={"attribute": "con", "priority": 1.5,
                    "startDate": time.strftime("%Y-%m-%d"), "text": "30-Day Ab/Squat Challenge", "type": "daily"})
print(json.dumps({k: v for k, v in req.json().items() if k in ['id', 'text', 'type']}, sort_keys=True))

for elem in sorted(schedule, key=itemgetter('day'), reverse=True):
    req = requests.post(args.baseurl + "tasks/user", headers=headers, json={"attribute": "con",
                        "date": time.strftime("%Y-%m-%d", time.localtime(time.time() + 24 * 3600 * (int(elem['day']) - 1))),
                        "notes": elem['notes'], "text": "30-Day Ab/Squat Challenge Day " + elem['day'], "type": "todo"})
    print(json.dumps({k: v for k, v in req.json().items() if k in ['date', 'id', 'text', 'type']}, sort_keys=True))
