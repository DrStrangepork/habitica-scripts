#!/usr/bin/env python

import json, os, requests, subprocess, time
#import pdb; pdb.set_trace()

USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")
TAG = "auto-forward"
TXT = "AUTO-FORWARDED"

headers = {"x-api-user":USR,"x-api-key":KEY,"Content-Type":"application/json"}

# Get autoforward tag id
tagsurl = "https://habitica.com/api/v3/tags"
req = requests.get(tagsurl, headers=headers)
for tag in (x for x in req.json()['data'] if x['name'] == TAG):
    TAGID = tag['id']

# Abort if autoforward tag not found
try:
    TAGID
except NameError:
    # print "Autoforward tag \"{}\" not found".format(TAG)
    quit()

# Abort if you are resting at the inn
userurl = "https://habitica.com/api/v3/user"
req = requests.get(userurl, headers=headers)
if req.json()['data']['preferences']['sleep']:
    # print "Resting in the Inn, autoforwarding cancelled"
    quit()

days = ("su", "m", "t", "w", "th", "f", "s")
# day of week (0..6); 0 is Sunday
daynum = int(time.strftime("%w"))
today = days[daynum]
yesterday = days[daynum-1]

# Get dailys
tasksurl = "https://habitica.com/api/v3/tasks/user?type=dailys"
req = requests.get(tasksurl, headers=headers)

for daily in (x for x in req.json()['data'] if TAGID in x['tags']):
    if daily['repeat'][yesterday] and daily['streak'] == 0:
        daily['repeat'][today] = True
        daily['text'] += " {}".format(TXT)
        taskurl = "https://habitica.com/api/v3/tasks/" + daily['id']
        task = requests.put(taskurl, headers=headers, data=json.dumps(daily))
