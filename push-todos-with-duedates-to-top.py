#!/usr/bin/env python

import os, requests, subprocess
#import pdb; pdb.set_trace()

USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

hab_url = "https://habitica.com/api/v3/tasks/user?type=todos"
headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}
duedate = unicode(subprocess.Popen(["date", "-I"], stdout=subprocess.PIPE).communicate()[0].strip(), "utf-8")

# MAIN
# Get todos
req = requests.get(hab_url, headers=headers)

duetoday = []

for todo in req.json()['data']:
    # To send only today's todos to the top:    todo['date'][:10] == duedate:
    # To send all overdue todos to the top:     todo['date'][:10] <= duedate:
    if 'date' in todo and todo['date'] and todo['date'][:10] <= duedate:
        duetoday.append(todo)

for todo in sorted(duetoday, key=lambda k: k['date'], reverse=True):
    toptaskurl = "https://habitica.com/api/v3/tasks/" + todo['id'] + "/move/to/0"
    toptask = requests.post(toptaskurl, headers=headers)
