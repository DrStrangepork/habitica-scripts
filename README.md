# habitica-scripts [![Build Status](https://travis-ci.org/DrStrangepork/habitica-scripts.svg?branch=master)](https://travis-ci.org/DrStrangepork/habitica-scripts)

Miscellaneous scripts for [Habitica](http://habitica.com)

## Contents

- 30-day.py
  - A 30-day escalating ab/squat exercise routine that creates:
    - One daily "30-Day Ab/Squat Challenge" to track your trend
    - One todo for each day of the Challenge
- am-i-on-a-quest.py
  - Are you participating in a quest or pending quest? Returns "Yes" or "No"
    - Can also return error codes 0 or 1 rather than "Yes" or "No"
- am-i-sleeping.py
  - Are you sleeping at the Inn? Returns "Yes" or "No"
    - Can also return error codes 0 or 1 rather than "Yes" or "No"
- autoforward-missed-dailys.py
  - Based on a specific tag, if a daily is missed, it will be added to the current day's dailys
  - For use with non-daily dailys, e.g. dailys that repeat every Monday
- cast-party-skills.py
  - Cast party skills (supercedes former cast-party-spells.py script)
- cast-party-spells-with-equip.py (formerly cast-party-spells.py)
  - Template for equipping a special set of armor to improve stats before casting party spells during a quest. The script is set to the ideal settings for my current avatar (lvl 69 Healer) - first, equip gear for peak CON then cast Protective Aura; second, equip gear for peak CON/INT then cast Blessing; finally, equip gear for peak STR to quest - but you can change it to what best suits your situation.
- get-group-data.py
  - Dumps group data to a file `group-data.json` in the current directory (default group: party)
- get-last-loggedin-timestamp.py
  - Displays your last loggedin timestamp (when you first logged in after your Custom Day Start time)
- get-tasks.py
  - Dumps your tasks to a file `user-tasks.json` in the current directory
- get-user-data.py
  - Dumps your user data to a file `user-data.json` in the current directory
- go-to-sleep.py
  - Go to sleep at the Inn
- habitica-backup.py
  - Backs up the JSON data export for offline storage
- party-health-check.sh
  - Checks the health of all party members and casts Blessing until all members are above a given threshold (default 30hp)
- push-todos-with-duedates-to-top.py
  - Moves active tasks with duedates to the top of the To-Dos list (excluding todos with future due dates)
- refill-health.py
  - Increases health points if less than given threshold
- refill-mana.py
  - Increases mana points if less than given threshold
- set-global-attribute-training.py
  - Sets the training attribute on your tasks to a given attribute (str, int, con, per)
- task-delete.sh
  - Simple bash script that deletes a given task ID

## Installation

- Install [Python 3](https://www.python.org/downloads/) and (possibly) [pip](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip)
- Clone the repo
  - `git clone https://github.com/DrStrangepork/habitica-scripts.git`
- Install pip packages
  - `pip install -r requirements.txt`

## Customize

These scripts access your Habitica account via the [Habitica API](https://habitica.com/apidoc/), so you must get your User ID and API Token from the [API Settings](https://habitica.com/#/options/settings/api) page of your account. You can either set the environment variables `HAB_API_USER` and `HAB_API_TOKEN` to your User ID and API Token or set them via the `-u` and `-k` arguments, respectively, on the command line (only for `*.py` scripts).

## shell/curl example

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
3. Add '--baseurl' argument to all
--->
