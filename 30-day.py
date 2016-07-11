#!/usr/bin/env python

import json, os, requests, time
from operator import itemgetter

USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

hab_url = "https://habitica.com/api/v3/tasks/user"
headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}
schedule = [
    {"day":"01","notes":"Crunches 10\nSit-ups 10\nSquats 25"},  {"day":"02","notes":"Crunches 15\nSit-ups 20\nSquats 30"},
    {"day":"03","notes":"Crunches 20\nSit-ups 5\nSquats 35"},   {"day":"04","notes":"Crunches 25\nSit-ups 10\nSquats 40"},
    {"day":"05","notes":"Crunches 10\nSit-ups 5\nSquats 30"},   {"day":"06","notes":"Crunches 30\nSit-ups 15\nSquats 50"},
    {"day":"07","notes":"Crunches 35\nSit-ups 20\nSquats 55"},  {"day":"08","notes":"Crunches 40\nSit-ups 30\nSquats 60"},
    {"day":"09","notes":"Rest Day"},                            {"day":"10","notes":"Crunches 10\nSit-ups 10\nSquats 25"},
    {"day":"11","notes":"Crunches 50\nSit-ups 40\nSquats 65"},  {"day":"12","notes":"Crunches 60\nSit-ups 45\nSquats 70"},
    {"day":"13","notes":"Crunches 5\nSit-ups 5\nSquats 5"},     {"day":"14","notes":"Crunches 10\nSit-ups 10\nSquats 10"},
    {"day":"15","notes":"Crunches 30\nSit-ups 20\nSquats 20"},  {"day":"16","notes":"Crunches 30\nSit-ups 25\nSquats 45"},
    {"day":"17","notes":"Crunches 50\nSit-ups 40\nSquats 60"},  {"day":"18","notes":"Rest Day"},
    {"day":"19","notes":"Crunches 5\nSit-ups 5\nSquats 5"},     {"day":"20","notes":"Crunches 10\nSit-ups 10\nSquats 25"},
    {"day":"21","notes":"Crunches 15\nSit-ups 20\nSquats 35"},  {"day":"22","notes":"Crunches 25\nSit-ups 20\nSquats 55"},
    {"day":"23","notes":"Crunches 40\nSit-ups 10\nSquats 55"},  {"day":"24","notes":"Crunches 50\nSit-ups 10\nSquats 65"},
    {"day":"25","notes":"Crunches 60\nSit-ups 15\nSquats 65"},  {"day":"26","notes":"Crunches 70\nSit-ups 20\nSquats 85"},
    {"day":"27","notes":"Rest Day"},                            {"day":"28","notes":"Crunches 80\nSit-ups 25\nSquats 95"},
    {"day":"29","notes":"Crunches 90\nSit-ups 30\nSquats 95"},  {"day":"30","notes":"Crunches 40\nSit-ups 40\nSquats 100"}
]

r = requests.post(hab_url, headers=headers, json={"attribute":"con","priority":1.5,
                  "startDate":time.strftime("%Y-%m-%d", time.localtime()),"text":"30-Day Ab/Squat Challenge","type":"daily"})
print json.dumps({k: v for k, v in r.json().items() if k in ['id','text','type']}, sort_keys=True)

for elem in sorted(schedule, key=itemgetter('day'), reverse=True):
    r = requests.post(hab_url, headers=headers, json={"attribute":"con",
                      "date":time.strftime("%Y-%m-%d", time.localtime(time.time() + 24*3600*(int(elem['day'])-1))),
                      "notes":elem['notes'],"text":"30-Day Ab/Squat Challenge Day "+elem['day'],"type":"todo"})
    print json.dumps({k: v for k, v in r.json().items() if k in ['date','id','text','type']}, sort_keys=True)
