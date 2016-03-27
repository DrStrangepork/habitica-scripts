# habitica-scripts
Miscellaneous scripts for Habitica

### Contents
- Habitica Task Reminder - task-reminder.py
    +  A python script that will parse through your tasks and email you reminders that you can control in Habitica. In the notes of any task, simply drop in a JSON key-value pair - `{"reminder":"20:00"}` - and if the task is not yet completed that day, you'll be sent an email to remind you! Also great for sending email pages to your cellphone!
- 30-day.py
    + A 30-day escalating ab/squat exercize routine that creates:
        * One daily task "30-Day Ab/Squat Challenge" to track your trend
        * One todo for each day of the Challenge
- task-delete.sh
    + Simple curl API wrapper for deleting tasks

### Examples
- To delete all unfinished todo's within a 30-day challenge:

```
for id in $(curl -H "x-api-key: $KEY" -H "x-api-user: $USR" -H "Content-Type:application/json" https://habitica.com:443/api/v2/user/tasks | \
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
