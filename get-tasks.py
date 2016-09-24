#!/usr/bin/env python

import json, os, requests, subprocess

USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}

# MAIN
req = requests.get("https://habitica.com/api/v3/tasks/user", headers=headers)
with open('hab_tasks.json', 'w') as f:
    json.dump(req.json(),f,separators=(',',':'),sort_keys=True)
