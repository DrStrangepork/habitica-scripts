#!/usr/bin/env python

import json, os, requests, subprocess
#import pdb; pdb.set_trace()

USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

# hab_url = "https://habitica.com/api/v3/user"
hab_url = "https://habitica.com/export/userdata.json"
headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}
HDB = "location_of_json_db"
TDB = "location_of_backup_json_db"
now = unicode(subprocess.Popen(["date", "-Iseconds"], stdout=subprocess.PIPE).communicate()[0].strip(), "utf-8")

# MAIN
# Load DB
with open(HDB, 'r') as f:
    DB = json.load(f)

# Get profile
req = requests.get(hab_url, headers=headers)

# Add profile
new = {}
new[now] = req.json()
DB.append(new)

# Save DB
#with open(TDB, 'w') as f:
with open(HDB, 'w') as f:
    json.dump(DB,f,separators=(',',':'),sort_keys=True)
