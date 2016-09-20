#!/usr/bin/env python

import json, os, requests, subprocess
# import pdb; pdb.set_trace()

USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

hab_url = "https://habitica.com/api/v3/user"
headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}

# MAIN
req = requests.get(hab_url, headers=headers)

# Save DB
with open('user-data.json', 'w') as f:
    json.dump(req.json(),f,separators=(',',':'),sort_keys=True)
