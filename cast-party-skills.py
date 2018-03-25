#!/usr/bin/env python2

import argparse
import os
import requests
import sys


parser = argparse.ArgumentParser(description="Cast party skills",
            epilog="See https://habitica.com/apidoc/#api-User-UserCast for the key map of class skills")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
parser.add_argument('-c', '--cast',
                    required=True,
                    choices=['all','both',
                            'earth','earthquake','mpheal','surge','etherealsurge',
                            'intimidate','intimidatinggaze','presence','valorousPresence',
                            'tools','toolsOfTrade','toolsofthetrade',
                            'blessing','healAll','protect','protectAura','protectiveaura'],
                    help='Spell(s) to cast')
parser.add_argument('-u', '--user-id',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_USER')
parser.add_argument('-k', '--api-token',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_TOKEN')
parser.add_argument('--baseurl',
                    type=str, default="https://habitica.com",
                    help='API server (default: https://habitica.com)')
parser.add_argument('--debug',
                    action=Debug, nargs=0,
                    help=argparse.SUPPRESS)
if len(sys.argv)==1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()
args.baseurl += "/api/v3/"

try:
    if args.user_id is None:
        args.user_id = os.environ['HAB_API_USER']
except KeyError:
    print "User ID must be set by the -u/--user-id option or by setting the environment variable 'HAB_API_USER'"
    sys.exit(1)

try:
    if args.api_token is None:
        args.api_token = os.environ['HAB_API_TOKEN']
except KeyError:
    print "API Token must be set by the -k/--api-token option or by setting the environment variable 'HAB_API_TOKEN'"
    sys.exit(1)


headers = {"x-api-user":args.user_id,"x-api-key":args.api_token,"Content-Type":"application/json"}

req = requests.get(args.baseurl + "user", headers=headers)

if req.json()['data']['stats']['class'] == "mage":
    if args.cast not in ("all","both","earth","earthquake","mpheal","etherealsurge"):
        print "Skill requested not available in character class"
        sys.exit(1)
      # Earthquake
    if args.cast in ("all","both","earth","earthquake"):
        skill = requests.post(args.baseurl + "user/class/cast/earth", headers=headers)
    # Ethereal Surge
    if args.cast in ("all","both","mpheal","etherealsurge"):
        skill = requests.post(args.baseurl + "user/class/cast/mpheal", headers=headers)
elif req.json()['data']['stats']['class'] == "warrior":
    if args.cast not in ("all","both","intimidate","intimidatinggaze","presence","valorousPresence"):
        print "Skill requested not available in character class"
        sys.exit(1)
    # Intimidating Gaze
    if args.cast in ("all","both","intimidate","intimidatinggaze"):
        skill = requests.post(args.baseurl + "user/class/cast/intimidate", headers=headers)
    # Valorous Presence
    if args.cast in ("all","both","presence","valorousPresence"):
        skill = requests.post(args.baseurl + "user/class/cast/valorousPresence", headers=headers)
elif req.json()['data']['stats']['class'] == "rogue":
    if args.cast not in ("all","both","tools","toolsOfTrade","toolsofthetrade"):
        print "Skill requested not available in character class"
        sys.exit(1)
    # Tools of the Trade
    if args.cast in ("all","both","tools","toolsOfTrade","toolsofthetrade"):
        skill = requests.post(args.baseurl + "user/class/cast/toolsOfTrade", headers=headers)
elif req.json()['data']['stats']['class'] == "healer":
    if args.cast not in ("all","both","protect","protectAura","protectiveaura","blessing","healAll"):
        print "Skill requested not available in character class"
        sys.exit(1)
    # Protective Aura
    if args.cast in ("all","both","protect","protectAura","protectiveaura"):
        skill = requests.post(args.baseurl + "user/class/cast/protectAura", headers=headers)
    # Blessing
    if args.cast in ("all","both","blessing","healAll"):
        skill = requests.post(args.baseurl + "user/class/cast/healAll", headers=headers)
