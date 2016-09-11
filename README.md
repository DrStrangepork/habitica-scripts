# habitica-scripts
Miscellaneous scripts for [Habitica](http://habitica.com)

### Contents
- 30-day.py
    + A 30-day escalating ab/squat exercize routine that creates:
        * One daily "30-Day Ab/Squat Challenge" to track your trend
        * One todo for each day of the Challenge
- habitica-backup.py
    + Backs up the JSON data export for offline storage
- push-todos-with-duedates-to-top.py
    + Moves active tasks with duedates to the top of the To-Dos list (excluding todos with future due dates)
- autoforward-missed-dailys.py
    + Based on a specific tag, if a daily is missed, it will be added to the current day's dailys
    + For use with non-daily dailys, e.g. dailys that repeat every Monday
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
