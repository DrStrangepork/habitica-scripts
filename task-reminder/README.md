#Habitica Task Reminder

A python script that will parse through your tasks and email you reminders that you can control in Habitica. In the notes of any task, simply drop in a JSON key-value pair - `{"reminder":"20:00"}` - and if the task is not yet completed that day, you'll be sent an email to remind you! If you already have notes written in the task, don't worry about adding the keypair, Habitica Task Reminder will find it appropriately.

The script will parse through all your tasks and send a simple email with the title of the text under the following conditions:

1. if 'type' == 'daily' and 'repeat' == today, or
2. if 'type' == 'todo' and (if 'date' == today or if there is no date assigned), then
3. check the time of the 'reminder'
4. If 'reminder' == now then send the reminder

##Installation
1. **Prerequisites:** `git`, `python` and `pip`
2. Install the Habitica Task Reminder from github: `git clone git@github.com:DrStrangepork/habitica-scripts.git`. The Habitica Task Reminder is in the `task-reminder` folder.
3. Install required python modules: `pip install -r requirements.txt`

#Configuration
1. Make the appropriate config changes for your Habitica and email accounts:

| Variable | Description |
| --- | --- |
| YOUR_USERID_HERE | Your User ID from https://habitica.com/#/options/settings/api |
| YOUR_KEY_HERE | Your API Token from https://habitica.com/#/options/settings/api |
| EMAIL_ACCT_ID | Email account user ID |
| EMAIL_ACCT_PW | Email account password |
| FROM_EMAIL_ADDRESS | your@address.com |
| TO_EMAIL_ADDRESS | Email address to remind |

You'll have to configure the script for your email carrier. The script should work fine on Google after you change your account to allow for [Less secure apps](https://www.google.com/settings/security/lesssecureapps) to sign into your account. Changing this setting may take a while to propagate through Gmail and allow you to login. If you get a SMTPAuthenticationError 534, you can fix it with [this link](https://accounts.google.com/DisplayUnlockCaptcha).

#Execution
1. Setup the `task-reminder.py` in your scheduler of choice (cron, SchedTasks, etc) at regular intervals. The frequency at which the script should run depends on your specifics with your notifications. If you know you'll only want to get notified at the top of any hour, then you could run the script only at the top of the hour. If you want to get notified at 6:18pm, then you'll probably need to run the script every minute. Personally, I run it every 15 minutes and set my reminders on the quarter-hours (":00",":15",":30",":45").
