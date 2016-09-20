#!/usr/bin/env python

import json, os, requests, subprocess, time
#import pdb; pdb.set_trace()


def unequip(gear):
    for k, v in gear.items():
        # If item ~ "base_0", you are already unequipped, so skip
        if "base_0" not in v:
            req = requests.post("https://habitica.com/api/v3/user/equip/equipped/{}".format(v), headers=headers)


USR = os.getenv('HAB_API_USER', "YOUR_USERID_HERE")
KEY = os.getenv('HAB_API_TOKEN', "YOUR_KEY_HERE")

headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}

aura = {
    "armor": "armor_healer_5",
    "head": "head_armoire_orangeCat",
    "shield": "shield_healer_5",
    "weapon": "weapon_armoire_basicCrossbow"
}
blessing = {
    "armor": "armor_healer_5",
    "head": "head_special_2",
    "shield": "shield_healer_5",
    "weapon": "weapon_healer_6"
}
quest = {
    "armor": "armor_special_finnedOceanicArmor",
    "head": "head_special_2",
    "shield": "shield_armoire_perchingFalcon",
    "weapon": "weapon_armoire_glowingSpear"
}

# MAIN
# First record what you're already wearing
req = requests.get("https://habitica.com/api/v3/user", headers=headers)
# If you "equip" what you're already wearing, you unequip it
unequip(req.json()['data']['items']['gear']['equipped'])

# Equip high CON gear to cast Protective Aura
for k, v in aura.items():
    req = requests.post("https://habitica.com/api/v3/user/equip/equipped/{}".format(v), headers=headers)

# Cast Protective Aura
#    Table of skillId. This may also be on the API doc page.
#    Mage
#      fireball: "Burst of Flames"
#      mpHeal: "Ethereal Surge"
#      earth: "Earthquake"
#      frost: "Chilling Frost"
#    Warrior
#      smash: "Brutal Smash"
#      defensiveStance: "Defensive Stance"
#      valorousPresence: "Valorous Presence"
#      intimidate: "Intimidating Gaze"
#    Rogue
#      pickPocket: "Pickpocket"
#      backStab: "Backstab"
#      toolsOfTrade: "Tools of the Trade"
#      stealth: "Stealth"
#    Healer
#      heal: "Healing Light"
#      protectAura: "Protective Aura"
#      brightness: "Searing Brightness"
#      healAll: "Blessing"
spell = requests.post("https://habitica.com/api/v3/user/class/cast/protectAura", headers=headers)

# Unequip your current gear to ensure that future equips really get equipped
unequip(req.json()['data']['gear']['equipped'])

# Equip high CON/INT gear to cast Blessing
for k, v in blessing.items():
    req = requests.post("https://habitica.com/api/v3/user/equip/equipped/{}".format(v), headers=headers)
spell = requests.post("https://habitica.com/api/v3/user/class/cast/healAll", headers=headers)
unequip(req.json()['data']['gear']['equipped'])

# Equip high STR gear for quest
for k, v in quest.items():
    req = requests.post("https://habitica.com/api/v3/user/equip/equipped/{}".format(v), headers=headers)
