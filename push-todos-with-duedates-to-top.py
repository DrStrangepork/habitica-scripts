#!/usr/bin/env python

import os, requests, subprocess, time
#import pdb; pdb.set_trace()

USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

todosurl = "https://habitica.com/api/v3/tasks/user?type=todos"
headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}
today = unicode(time.strftime("%Y-%m-%d"))

# MAIN
# Get todos
req = requests.get(todosurl, headers=headers)

duetoday = []

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
