#!/usr/bin/env python3

import argparse
import os
import re
import sys
import time
import requests


def collect_pets(items, food_type):
    pets_to_feed = {}
    for name, value in items['pets'].items():
        # Skip feeding pets of mounts
        if name in items['mounts']:
            continue
        if food_type in name:
            pets_to_feed[name] = value
    # pets_to_feed_sorted = dict(sorted(pets_to_feed.items(), key=lambda item: item[1], reverse=True))
    return dict(sorted(pets_to_feed.items(), key=lambda item: item[1], reverse=True))


def feed_pets(items, pets, food, url, headers):
    if not pets.keys():
        print(f'No pets want to eat {food}')
        return
    for pet in pets.keys():
        while items['food'][food] > 0:
            try:
                feed_food = requests.post(f'{url}user/feed/{pet}/{food}', headers=headers)
                feed_food.raise_for_status()
                # If no errors, then food was consumed
                items['food'][food] -= 1
                # Avoid TooManyRequests/rate limit errors
                time.sleep(2)
                if feed_food.json()['data'] > 0:
                    print(f"{feed_food.json()['message']} ({feed_food.json()['data'] / 50 * 100})")
                else:
                    print(f"{feed_food.json()['message']}")
                    items['mounts'][pet] = True
                    break
            except requests.exceptions.RequestException:
                if 'TooManyRequests' in feed_food.json():
                    print('Sleeping for 60s due to rate limiting restrictions')
                    time.sleep(60)
                else:
                    print(feed_food.json())
                    sys.exit(1)


# MAIN
parser = argparse.ArgumentParser(description='Feed hungry pets with all available food items')
parser.add_argument('-u', '--user-id',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_USER')
parser.add_argument('-k', '--api-token',
                    help='From https://habitica.com/#/options/settings/api\n \
                    default: environment variable HAB_API_TOKEN')
parser.add_argument('--baseurl',
                    type=str, default="https://habitica.com",
                    help='API server (default: https://habitica.com)')
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

req = requests.get(args.baseurl + "user", headers=headers)
items = req.json()['data']['items']

# for food in ["RottenMeat"]:
for food in items['food']:
    if items['food'][food] == 0:
        continue
    if food == 'Meat' or 'Base' in food:
        feed_pets(items, collect_pets(items, 'Base'), food, args.baseurl, headers)
    elif food == 'Milk' or 'White' in food:
        feed_pets(items, collect_pets(items, 'White'), food, args.baseurl, headers)
    elif food == 'Potatoe' or 'Desert' in food:
        feed_pets(items, collect_pets(items, 'Desert'), food, args.baseurl, headers)
    elif food == 'Strawberry' or 'Red' in food:
        feed_pets(items, collect_pets(items, 'Red'), food, args.baseurl, headers)
    elif food == 'Chocolate' or 'Shade' in food:
        feed_pets(items, collect_pets(items, 'Shade'), food, args.baseurl, headers)
    elif food == 'Fish' or 'Skeleton' in food:
        feed_pets(items, collect_pets(items, 'Skeleton'), food, args.baseurl, headers)
    elif food == 'RottenMeat' or 'Zombie' in food:
        feed_pets(items, collect_pets(items, 'Zombie'), food, args.baseurl, headers)
    elif food == 'CottonCandyPink' or 'CottonCandyPink' in food:
        feed_pets(items, collect_pets(items, 'CottonCandyPink'), food, args.baseurl, headers)
    elif food == 'CottonCandyBlue' or 'CottonCandyBlue' in food:
        feed_pets(items, collect_pets(items, 'CottonCandyBlue'), food, args.baseurl, headers)
    elif food == 'Honey' or 'Golden' in food:
        feed_pets(items, collect_pets(items, 'Golden'), food, args.baseurl, headers)
