#!/usr/bin/env python

party_damage_done = 0
chat_index = 0

# -X GET https://habitica.com/api/v3/groups/party
# party = {
#     "data": {
#         "chat": [
#             {
#                 "flagCount": 0,
#                 "flags": {},
#                 "id": "79e71039-86b5-4b14-a110-a9b7fc232cfb",
#                 "likes": {},
#                 "text": "`MidnightBlaze attacks Fire Skull Swarm for 221.4 damage.` `Fire Skull Swarm attacks party for 2.1 damage.`",
#                 "timestamp": 1477749789192,
#                 "uuid": "system"
#             },
#             {
#                 "flagCount": 0,
#                 "flags": {},
#                 "id": "90c79b5b-e5c6-4478-8380-7da34da0c839",
#                 "likes": {},
#                 "text": "`NotBatman101 attacks Fire Skull Swarm for 6.0 damage.` `Fire Skull Swarm attacks party for 3.9 damage.`",
#                 "timestamp": 1477748298398,
#                 "uuid": "system"
#             }
#         ],
#         "quest": {
#             "active": true,
#             "extra": {},
#             "key": "taskwoodsTerror1",
#             "leader": "a9f44ccf-ee23-42fc-bf14-39bd8ac9691d",
#             "members": {
#                 "108e1bf5-d773-4011-8a96-e2d4b4da9a30": true,
#                 "1b594caa-b03e-4ac8-b84b-2fdd148dc580": true,
#                 "301ae670-9c4a-4e79-8471-5c45e8294af7": true,
#                 "30983c37-52c3-415d-977c-38af6c7db91c": true,
#                 "45ab7466-7035-4c61-a3db-007d2956d856": true,
#                 "6e483790-e4ba-4fd2-b5d7-00b72d0a2c3a": true,
#                 "70ccdaba-d127-490e-bb7b-95a41f1c5ed5": true,
#                 "771e0321-3d69-4a99-98e7-f159717c6b25": true,
#                 "91c0c627-cdf0-4550-8596-819c7f3e3958": true,
#                 "a9f44ccf-ee23-42fc-bf14-39bd8ac9691d": true,
#                 "b854c026-04a5-4c70-89f4-9b4a6439a7b5": true,
#                 "b878fab1-3185-466b-915f-fd6f4a94c248": true,
#                 "e0d41c8e-5d2a-42a1-8d0d-bde0f5c1046d": true
#             },
#             "progress": {
#                 "collect": {},
#                 "hp": 114.20082564781535,
#                 "rage": 23.177799749246912
#             }
#         }
#     }
# }

if party[data][quest][active]:
    boss = party[data][quest][key]
    boss_hp = party[data][quest][progress][hp]
    # -X GET https://habitica.com/api/v3/content
    # quest = {
    #     "data": {
    #         "quests": {
    #             "taskwoodsTerror1": {     # <-- party[data][quest][key]
    #                 "boss": {
    #                     "def": 1,
    #                     "hp": 500,
    #                     "name": "Fire Skull Swarm",
    #                     "rage": {
    #                         "description": "Swarm Respawn: This bar fills when you don't complete your Dailies. When it is full, the Fire Skull Swarm will heal 30% of its remaining health!",
    #                         "effect": "`Fire Skull Swarm uses SWARM RESPAWN!`\n\nEmboldened by their victories, more skulls swirl around you in a gout of flame!",
    #                         "healing": 0.3,
    #                         "title": "Swarm Respawn",
    #                         "value": 50
    #                     },
    #                     "str": 1
    #                 },
    #                 "category": "gold",
    #                 "completion": "With the help of the Joyful Reaper and the renowned pyromancer @Beffymaroo, you manage to drive back the swarm. In a show of solidarity, Beffymaroo offers you her Pyromancer's Turban as you move deeper into the forest.",
    #                 "drop": {
    #                     "exp": 500,
    #                     "gp": 0,
    #                     "items": [
    #                         {
    #                             "key": "Skeleton",
    #                             "text": "Skeleton Hatching Potion",
    #                             "type": "hatchingPotions"
    #                         },
    #                         {
    #                             "key": "Red",
    #                             "text": "Red Hatching Potion",
    #                             "type": "hatchingPotions"
    #                         },
    #                         {
    #                             "key": "head_special_pyromancersTurban",
    #                             "text": "Pyromancer's Turban (Headgear)",
    #                             "type": "gear"
    #                         }
    #                     ]
    #                 },
    #                 "goldValue": 200,
    #                 "key": "taskwoodsTerror1",
    #                 "notes": "You have never seen the Joyful Reaper so agitated. The ruler of the Flourishing Fields lands her skeleton gryphon mount right in the middle of Productivity Plaza and shouts without dismounting. \"Lovely Habiticans, we need your help! Something is starting fires in the Taskwoods, and we still haven't fully recovered from our battle against Burnout. If it's not halted, the flames could engulf all of our wild orchards and berry bushes!\"<br><br>You quickly volunteer, and hasten to the Taskwoods. As you creep into Habitica’s biggest fruit-bearing forest, you suddenly hear clanking and cracking voices from far ahead, and catch the faint smell of smoke. Soon enough, a horde of cackling, flaming skull-creatures flies by you, biting off branches and setting the treetops on fire!",
    #                 "text": "Terror in the Taskwoods, Part 1: The Blaze in the Taskwoods",
    #                 "value": 4
    #             }
    #         }
    #     }
    # }
    boss_starting_hp = quest[data][quests][{party[data][quest][key]}][boss][hp]
    attacks = {}
    while boss_hp + party_damage_done >= boss_starting_hp:
        # text = party[data][chat][chat_index][text]
        # Parse party[data][chat][chat_index][text] as a string that contains a 2-element array, "`elem1` `elem2`"
        # We only care about elem1
        if elem1 ~= "/ attacks (\w+ )* for [0-9\.]+ damage/":
            member = split(" ",elem1)[0]
            damage = split(" ",elem1)[-2]     # Second-to-last element
            if attacks[member]:
                attacks[member] += attack.damage
            else:
                attacks[member] = attack.damage
            party_damage_done += attack.damage
        chat_index++

# "attacks": {"Member1": "10","Member2": "1"}
