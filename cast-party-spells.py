#!/usr/bin/env python
# See https://habitica.com/apidoc/#api-User-UserCast for the key map of class spells

import argparse, os, requests, sys
parser = argparse.ArgumentParser(description="Template for equipping a special set of armor \
                                 to improve stats before casting party spells during a quest")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


def unequip(gear):
    for k, v in gear.items():
        # If item ~ "base_0", you are already unequipped, so skip
        if "base_0" not in v:
            req = requests.post("https://habitica.com/api/v3/user/equip/equipped/{}".format(v), headers=headers)


# MAIN
# Use the environment variable HAB_API_USER,
# otherwise replace YOUR_USERID_HERE with your User ID
USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
# Use the environment variable HAB_API_TOKEN,
# otherwise replace YOUR_KEY_HERE with your API token
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

parser.add_argument('-c','--cast', \
                    required=True, \
                    choices=['all','both','none','blessing','healAll','protectAura','protectiveaura'], \
                    help='Spell(s) to cast')
parser.add_argument('-u','--user-id', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('-k','--api-token', \
                    help='From https://habitica.com/#/options/settings/api')
parser.add_argument('--debug', \
                    action=Debug, nargs=0, \
                    help=argparse.SUPPRESS)
if len(sys.argv)==1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()

if args.user_id is not None:
    USR = args.user_id

if args.api_token is not None:
    KEY = args.api_token

headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}

aura = {
    "armor": "armor_special_2",
    "head": "head_armoire_orangeCat",
    "shield": "shield_special_goldenknight",
    "weapon": "weapon_armoire_basicCrossbow"
}
blessing = {
    "armor": "armor_special_2",
    "head": "head_special_2",
    "shield": "shield_special_goldenknight",
    "weapon": "weapon_healer_6"
}
quest = {
    "armor": "armor_special_finnedOceanicArmor",
    "head": "head_special_2",
    "shield": "shield_armoire_perchingFalcon",
    "weapon": "weapon_special_2"
}

# First record what you're already wearing
req = requests.get("https://habitica.com/api/v3/user", headers=headers)
# If you "equip" what you're already wearing, you unequip it
unequip(req.json()['data']['items']['gear']['equipped'])

# Protective Aura
if args.cast in ("all","both","protectAura","protectiveaura"):
    for k, v in aura.items():
        req = requests.post("https://habitica.com/api/v3/user/equip/equipped/{}".format(v), headers=headers)
    spell = requests.post("https://habitica.com/api/v3/user/class/cast/protectAura", headers=headers)
    unequip(req.json()['data']['gear']['equipped'])

# Blessing
if args.cast in ("all","both","blessing","healAll"):
    for k, v in blessing.items():
        req = requests.post("https://habitica.com/api/v3/user/equip/equipped/{}".format(v), headers=headers)
    spell = requests.post("https://habitica.com/api/v3/user/class/cast/healAll", headers=headers)
    unequip(req.json()['data']['gear']['equipped'])

# Equip for quest
for k, v in quest.items():
    req = requests.post("https://habitica.com/api/v3/user/equip/equipped/{}".format(v), headers=headers)
