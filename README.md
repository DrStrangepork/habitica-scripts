# habitica-scripts [![Build Status](https://travis-ci.org/DrStrangepork/habitica-scripts.svg?branch=master)](https://travis-ci.org/DrStrangepork/habitica-scripts)
Miscellaneous scripts for [Habitica](http://habitica.com)

### Contents
- 30-day.py
    + A 30-day escalating ab/squat exercize routine that creates:
        * One daily "30-Day Ab/Squat Challenge" to track your trend
        * One todo for each day of the Challenge
- am-i-sleeping.py
    + Are you sleeping at the Inn? Returns "Yes" or "No"
        * Can also return error codes 0 or 1 rather than "Yes" or "No"
- autoforward-missed-dailys.py
    + Based on a specific tag, if a daily is missed, it will be added to the current day's dailys
    + For use with non-daily dailys, e.g. dailys that repeat every Monday
- cast-party-spells.py
    + Template for equipping a special set of armor to improve stats before casting party spells during a quest. The script is set to the ideal settings for my current avatar (lvl 69 Healer) - first, equip gear for peak CON then cast Protective Aura; second, equip gear for peak CON/INT then cast Blessing; finally, equip gear for peak STR to quest - but you can change it to what best suits your situation.
- get-tasks.py
    + Dumps your tasks to a file `hab_tasks.json` in the current directory
- get-user-data.py
    + Dumps your user data to a file `user-data.json` in the current directory
- habitica-backup.py
    + Backs up the JSON data export for offline storage
- push-todos-with-duedates-to-top.py
    + Moves active tasks with duedates to the top of the To-Dos list (excluding todos with future due dates)
- set-global-attribute-training.py
    + Sets the training attribute on your tasks to a given attribute (str, int, con, per)

### Installation
- Install [Python](https://www.python.org/downloads/) and (possibly) [pip](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip)
    + Scripts have been tested with python 2.7 but should work with 3.x
- Clone the repo
    + `git clone https://github.com/DrStrangepork/habitica-scripts.git`
- Install pip packages
    + `pip install -r requirements.txt`

### Customize
These scripts access your Habitica account via the [Habitica API](https://habitica.com/apidoc/), so you must configure them with your [Habitica User ID and API Token](https://habitica.com/#/options/settings/api):
```
USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")
```

The variables USR and KEY map to your User ID and API Token, respectively. You can either set the environment variables `HAB_API_USER` and `HAB_API_TOKEN` to your User ID and API Token or change the strings "YOUR_USERID_HERE" and "YOUR_KEY_HERE" to your User ID and API Token.

### shell/curl example
- To delete all unfinished todo's within a 30-day challenge:
```
for id in $(curl -H "x-api-key: $HAB_API_TOKEN" -H "x-api-user: $HAB_API_USER" -H "Content-Type:application/json" https://habitica.com/api/v3/tasks/user | \
        jq -r '.[] | select(.type == "todo") | select(.text | startswith("30-Day Ab/Squat Challenge")) | select(.completed == false) | .id' | \
        sed 's/\\r//g'); do
    task-delete.sh $id
done
```
- The above requires [jq](https://stedolan.github.io/jq/) and the environment variable settings mentioned above

<!---
### To-do
1. Create authentication scheme similar to AWS CLI (for saving API keys)
2. Add task up/down scripts
--->
