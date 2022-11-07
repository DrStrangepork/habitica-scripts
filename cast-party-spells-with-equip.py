#!/usr/bin/env python3

import argparse
import os
import re
import sys
import requests


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


def unequip(gear):
    for k, v in gear.items():
        # If item ~ "base_0", you are already unequipped, so skip
        if "base_0" not in v:
            requests.post(args.baseurl + f'user/equip/equipped/{v}', headers=headers)


# MAIN
parser = argparse.ArgumentParser(description="Template for equipping a special set of armor \
                                 to improve stats before casting party spells during a quest",
                                 epilog="See https://habitica.com/apidoc/#api-User-UserCast for the key map of class spells")
parser.add_argument('-c', '--cast',
                    required=True,
                    choices=['all', 'both', 'none', 'blessing', 'healAll', 'protect', 'protectAura', 'protectiveaura'],
                    help='Spell(s) to cast')
parser.add_argument('-b', '--bossquest',
                    action='store_true',
                    help='Equip a special equipment set for fighting bosses')
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
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()
args.baseurl += "/api/v3/"

try:
    if args.user_id is None:
        args.user_id = os.environ['HAB_API_USER']
    if not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', args.user_id, re.IGNORECASE):
        print(f"Invalid User ID: '{args.user_id}'")
        sys.exit(1)
except KeyError:
    print("User ID must be set by the -u/--user-id option or by setting the environment variable 'HAB_API_USER'")
    sys.exit(1)

try:
    if args.api_token is None:
        args.api_token = os.environ['HAB_API_TOKEN']
    if not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', args.api_token, re.IGNORECASE):
        print(f"Invalid API Token: '{args.api_token}'")
        sys.exit(1)
except KeyError:
    print("API Token must be set by the -k/--api-token option or by setting the environment variable 'HAB_API_TOKEN'")
    sys.exit(1)


headers = {"x-api-user": args.user_id, "x-api-key": args.api_token, "Content-Type": "application/json"}

# Max out Constitution
aura = {
    "armor": "armor_healer_5",
    "head": "head_armoire_orangeCat",
    "shield": "shield_special_goldenknight",
    "weapon": "weapon_armoire_blueLongbow"
}
# Max out Constitution and Intelligence
blessing = {
    "armor": "armor_special_2",
    "head": "head_special_2",
    "shield": "shield_special_goldenknight",
    "weapon": "weapon_healer_6"
}
# Max out Strength
bossquest = {
    "armor": "armor_special_finnedOceanicArmor",
    "head": "head_special_2",
    "shield": "shield_armoire_perchingFalcon",
    "weapon": "weapon_special_2"
}
# Max out all attributes
quest = {
    "armor": "armor_special_2",
    "head": "head_special_2",
    "shield": "shield_special_goldenknight",
    "weapon": "weapon_special_2"
}

# If bossquest, then set questing equipment set to that
if args.bossquest:
    quest = bossquest

# First record what you're already wearing
req = requests.get(args.baseurl + "user", headers=headers)
# If you "equip" what you're already wearing, you unequip it
unequip(req.json()['data']['items']['gear']['equipped'])

# Protective Aura
if args.cast in ("all", "both", "protect", "protectAura", "protectiveaura"):
    for k, v in aura.items():
        req = requests.post(args.baseurl + f'user/equip/equipped/{v}', headers=headers)
    spell = requests.post(args.baseurl + "user/class/cast/protectAura", headers=headers)
    unequip(req.json()['data']['gear']['equipped'])

# Blessing
if args.cast in ("all", "both", "blessing", "healAll"):
    for k, v in blessing.items():
        req = requests.post(args.baseurl + f'user/equip/equipped/{v}', headers=headers)
    spell = requests.post(args.baseurl + "user/class/cast/healAll", headers=headers)
    unequip(req.json()['data']['gear']['equipped'])

# Equip for quest
for k, v in quest.items():
    req = requests.post(args.baseurl + f'user/equip/equipped/{v}', headers=headers)
