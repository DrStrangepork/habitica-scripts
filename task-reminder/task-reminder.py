#!/usr/bin/env python

import ast, json, os, re, requests, smtplib
from time import localtime, strftime

USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

hab_url = "https://habitica.com/api/v2/user/tasks"
headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}
mail_id = 'EMAIL_ACCT_ID'       # Email account user ID
mail_pw = 'EMAIL_ACCT_PW'       # Email account password
FROM = 'FROM_EMAIL_ADDRESS'     # your@address.com or mail_id
TO = 'TO_EMAIL_ADDRESS'         # Email address to remind


def _due_today(task):
    #task['date'] = "2016-04-30T04:00:00.000Z",
    #todate       = "2016-04-30"
    due_today = False
    if not task.has_key('date') or not task['date']:
        due_today = True
    elif task['date'].split("T")[0] == todate:
        due_today = True

    return due_today


def _repeat_today(task):
    repeat_today = False
    if today == "Mon" and task['repeat']['m']:
        repeat_today = True
    elif today == "Tue" and task['repeat']['t']:
        repeat_today = True
    elif today == "Wed" and task['repeat']['w']:
        repeat_today = True
    elif today == "Thu" and task['repeat']['th']:
        repeat_today = True
    elif today == "Fri" and task['repeat']['f']:
        repeat_today = True
    elif today == "Sat" and task['repeat']['s']:
        repeat_today = True
    elif today == "Sun" and task['repeat']['su']:
        repeat_today = True

    return repeat_today


def send_reminder(task):
    """ Send the reminder to the TO address
    """
    # Prepare actual message
    # Subject: \n\n%s     Subj == '', Body == text (good for texting)
    # Subject: %s\n\n     Subj == test, Body == '' (good for email)
    message = """\From: %s\nTo: %s\nSubject: \n\n%s
    """ % (FROM, TO, task['text'])

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(mail_id, mail_pw)
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        print "failed to send mail"


# MAIN
now     = strftime("%H:%M", localtime())    # '16:20'
today   = strftime("%a", localtime())       # 'Wed'
todate  = strftime("%Y-%m-%d", localtime()) # '2016-04-20'

tasks = requests.get(hab_url, headers=headers)

for task in (x for x in tasks.json() if \
                ((x['type'] == "daily" and _repeat_today(x)) \
                    or (x['type'] == "todo" and _due_today(x))) \
                    and not x['completed']
            ):
    m = re.search('\{.*\}',task['notes'])
    if m and ast.literal_eval(m.group(0)).has_key('reminder'):
        if ast.literal_eval(m.group(0))['reminder'] == now:
            send_reminder(task)
