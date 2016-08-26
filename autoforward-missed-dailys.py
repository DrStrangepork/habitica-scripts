#!/usr/bin/env python

import os, requests, subprocess
#import pdb; pdb.set_trace()


# Return True if there was a history event yesterday (the task was checked)
def bHistoryYesterday(task):
    if not task['history']:
        return False
    else:
        # We only want the first 10 characters of the epoch date string
        latest_history = int(str(task['history'][-1]['date'])[0:10])
        # latest_history = 1471683605
        latest_history_date = int(unicode(subprocess.Popen(["date", "-I", "--date='{}'".format(latest_history)], stdout=subprocess.PIPE).communicate()[0].strip(), "utf-8"))
        return latest_history_date == duedate


USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")
TAG = "auto-forward"
TXT = "AUTO-FORWARDED"

headers = {"x-api-user":USR,"x-api-key":KEY,"Content-Type":"application/json"}

# Get autoforward tag
tagsurl = "https://habitica.com/api/v3/tags"
req = requests.get(tagsurl, headers=headers)
for tag in (x for x in req.json()['data'] if x['name'] == TAG):
    TAGID = tag['id']

try:
    TAGID
except NameError:
    print "Autoforward tag \"{}\" not found".format(TAG)
    quit()

duedate = unicode(subprocess.Popen(["date", "-I", "--date=yesterday"], stdout=subprocess.PIPE).communicate()[0].strip(), "utf-8")
# day of week (0..6); 0 is Sunday
daynum = int(unicode(subprocess.Popen(["date", "+%w"], stdout=subprocess.PIPE).communicate()[0].strip(), "utf-8"))
days = ("su", "m", "t", "w", "th", "f", "s")

today = days[daynum]
dueday = days[daynum-1]

# Get dailys
tasksurl = "https://habitica.com/api/v3/tasks/user?type=dailys"
req = requests.get(tasksurl, headers=headers)

for daily in req.json()['data']:
    if daily['repeat'][dueday] and TAGID in daily['tags'] and not bHistoryYesterday(daily):
        daily['repeat'][today] = True
        daily['text'] += " {}".format(TXT)
        taskurl = "https://habitica.com/api/v3/tasks/" + daily['id']
        task = requests.put(taskurl, headers=headers, data=json.dumps(daily))
