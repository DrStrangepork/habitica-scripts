# habitica-scripts
Miscellaneous scripts for Habitica

### Installation
- Execute `pip install -r requirements.txt`

### Contents
- 30-day.py
    + A 30-day escalating ab/squat exercize routine that creates:
        * One daily task "30-Day Ab/Squat Challenge" to track your trend
        * One todo for each day of the Challenge
- task-delete.sh
    + Simple curl API wrapper for deleting tasks
- habitica-backup.py
    + Backs up the JSON data export for offline storage
- push-todos-with-duedates-to-top.py
    + Moves active tasks with duedates to the top of the To-Dos list (excluding todos with future due dates)
- autoforward-missed-dailys.py
    + Based on a specific tag, if a daily is missed, it will be added to the current day's dailys
    + For use with non-daily dailys, e.g. dailys that repeat every Monday

### Examples
- To delete all unfinished todo's within a 30-day challenge:

```
for id in $(curl -H "x-api-key: $KEY" -H "x-api-user: $USR" -H "Content-Type:application/json" https://habitica.com/api/v3/tasks/user | \
        jq -r '.[] | select(.type == "todo") | select(.text | startswith("30-Day Ab/Squat Challenge")) | select(.completed == false) | .id' | \
        sed 's/\\r//g'); do
    task-delete.sh $id
done
```

<!---
### To-do
1. Create authentication scheme similar to AWS CLI (for saving API keys)
2. Add task up/down scripts
--->
