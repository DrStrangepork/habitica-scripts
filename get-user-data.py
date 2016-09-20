#!/usr/bin/env python

import json, os, requests, subprocess
# import pdb; pdb.set_trace()

USR = os.getenv('HAB_API_USER', "30983c37-52c3-415d-977c-38af6c7db91c")
KEY = os.getenv('HAB_API_TOKEN', "1d60df4c-a352-4ae4-900a-f2a93c955453")

hab_url = "https://habitica.com/api/v3/user"
headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}

# MAIN
req = requests.get(hab_url, headers=headers)

# Save DB
with open('user-data.json', 'w') as f:
    json.dump(req.json(),f,separators=(',',':'),sort_keys=True)
