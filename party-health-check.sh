#!/bin/bash
VALUE=30
QUIET=false

usage() {
  echo \
"$(tput bold)$(basename ${BASH_SOURCE[0]})$(tput sgr0)
Usage:  Checks the health of all party members and casts Blessing
        until all members are above a given threshold (default 30hp)
Example:  $(basename ${BASH_SOURCE[0]}) -v 45
Options:
  -v HP         Minimum threshold HP for all party members
  -q            quiet (no output)
  -h            help"
}

curlh() {
    curl -s --compressed -H "x-api-key:$HAB_API_TOKEN" -H "x-api-user:$HAB_API_USER" -H "Content-Type:application/json" $*
}

get_hp() {
    echo $(curlh -X GET https://habitica.com/api/v3/members/$1 | jq -r '.data.stats.hp')
}

get_name() {
    echo $(curlh -X GET https://habitica.com/api/v3/members/$1 | jq -r '.data.profile.name')
}

isPositiveNumber() {
    if (( $(echo "$1 == $1 && $1 > 0" | bc -l 2>/dev/null) )); then
        return 0
    else
        return 1
    fi
}


prereq="Prerequisites are missing and must be installed before continuing:\n"
missing_req=false
if ! which jq >/dev/null 2>&1; then
    prereq+="\t'jq' from https://stedolan.github.io/jq/\n"
    missing_req=true
fi
if $missing_req; then
    echo -e "Error: $prereq" >&2
    exit 1
fi


[[ "$@" =~ "--help" ]] && { usage | less; exit; }
while getopts ":qv:h" opt; do
    case $opt in
        q)  QUIET=true
            ;;
        v)  if isPositiveNumber $OPTARG; then
                VALUE=$OPTARG
            else
                echo "Error: $OPTARG must be a positive number" >&2
                usage ; exit 1
            fi
            ;;
        h)  usage ; exit
            ;;
        *)  echo "Error: invalid option -$OPTARG" >&2
            usage ; exit 1
            ;;
    esac
done


for member in $(curlh -X GET https://habitica.com/api/v3/groups/party | jq -r '.data.quest.members | keys[]'); do
    name=$(get_name $member)
    hp=$(get_hp $member)
    while (( $(echo "$hp <= $VALUE" | bc -l) )); do
        $QUIET || printf "%s:%s\n" $name $hp
        cast-party-spells.py -c blessing
        hp=$(get_hp $member)
    done
done
