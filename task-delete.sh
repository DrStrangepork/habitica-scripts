#!/bin/bash
USR=YOUR_USERID_HERE
KEY=YOUR_KEY_HERE

curl -X DELETE -H "x-api-key: $KEY" -H "x-api-user: $USR" -H "Content-Type:application/json" https://habitica.com/api/v2/user/tasks/{$1}; echo;
