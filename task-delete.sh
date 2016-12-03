#!/bin/bash

curl -X DELETE -H "x-api-key: $KEY" -H "x-api-user: $USR" -H "Content-Type:application/json" https://habitica.com/api/v3/tasks/:{$1}; echo;
