#!/usr/bin/env python

import ast, json, os, re, requests, smtplib
from time import localtime, strftime

USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

hab_url = "https://habitica.com/api/v2/user/tasks"
headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}
reminders_db = "reminders.json" # List of dicts
                                #   [
                                #     {
                                #       "id": "f3dba77e-442c-8ae0-c96b-d19fdc154561",
                                #       "reminder": "24-hour time, ex 20:00",
                                #       "text": "task title"
                                #     }
                                #   ]
mail_id = EMAIL_ACCT_ID         # Email account user ID
mail_pw = EMAIL_ACCT_PW         # Email account password
FROM = FROM_EMAIL_ADDRESS       # your@address.com or mail_id
TO = TO_EMAIL_ADDRESS           # Email address to remind


# Runs every minute
def send_reminders(reminders):
    for item in reminders:
        if item['reminder'] == now:
            # Prepare actual message
            # Subject: \n\n%s     Subj == '', Body == text (good for texting)
            # Subject: %s\n\n     Subj == test, Body == '' (good for email)
            message = """\From: %s\nTo: %s\nSubject: \n\n%s
            """ % (FROM, TO, item['text'])

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login(mail_id, mail_pw)
                server.sendmail(FROM, TO, message)
                server.close()
            except:
                print "failed to send mail"


def check_reminders(reminders):
    r = requests.get(hab_url, headers=headers)
    for task in r.json():
        m = re.search('\{.*\}',task['notes'])
        if m and ast.literal_eval(m.group(0)).has_key('reminder'):
            if task.has_key('completed') and task['completed']:
                # if "completed": true, delete from reminders and ignore task
                reminders = list(filter(lambda x: x['id'] != task['id'], reminders))
            else:
                # add/update the reminder
                new = {}
                new['id'] = task['id']
                new['text'] = task['text']
                new['reminder'] = ast.literal_eval(m.group(0))['reminder']
                reminders.append(new)

    # Remove duplicate task id's
    # Because updates are appended, changes made on Habitica will update database here
    reminders = {v['id']:v for v in reminders}.values()

    with open(reminders_db, 'w') as data_file:
        json.dump(reminders, data_file)


# MAIN
now = strftime("%H:%M", localtime())
with open(reminders_db) as data_file:
    reminders = json.load(data_file)

send_reminders(reminders)
# Every hour, get tasks and update reminders
if re.search(':00',now):
    check_reminders(reminders)
