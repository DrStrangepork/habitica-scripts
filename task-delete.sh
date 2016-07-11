#!/bin/bash
USR=${HAB_API_USER-YOUR_USERID_HERE}
KEY=${HAB_API_TOKEN-YOUR_KEY_HERE}

curl -X DELETE -H "x-api-key: $KEY" -H "x-api-user: $USR" -H "Content-Type:application/json" https://habitica.com/api/v3/tasks/:{$1}; echo;
