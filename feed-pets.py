#!/usr/bin/env python3

import argparse
import os
import requests
import sys
import time


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


def collect_pets(items, filter):
    pets_to_feed = {}
    for name,value in items['pets'].items():
        # Skip feeding pets of mounts
        if name in items['mounts']:
            continue
        if filter in name:
            pets_to_feed[name] = value
    # pets_to_feed_sorted = dict(sorted(pets_to_feed.items(), key=lambda item: item[1], reverse=True))
    return dict(sorted(pets_to_feed.items(), key=lambda item: item[1], reverse=True))


def feed_pets(items, pets, food, url, headers):
    for pet in pets.keys():
        while (items['food'][food] > 0):
            try:
                p = requests.post("%suser/feed/%s/%s" % (url, pet, food), headers=headers)
                p.raise_for_status()
                # If no errors, then food was consumed
                items['food'][food] -= 1
                # Avoid TooManyRequests/rate limit errors
                time.sleep(2)
                if p.json()['data'] > 0:
                    print('%s (%d%%)' % (p.json()['message'], p.json()['data']/50*100))
                else:
                    print('%s' % p.json()['message'])
                    items['mounts'][pet] = True
                    break
            except requests.exceptions.RequestException:
                if 'TooManyRequests' in p.json():
                    print('Sleeping for 60s due to rate limiting restrictions')
                    time.sleep(60)
                else:
                    print(p.json())
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
parser.add_argument('--debug',
                    action=Debug, nargs=0,
                    help=argparse.SUPPRESS)
args = parser.parse_args()
args.baseurl += "/api/v3/"

try:
    if args.user_id is None:
        args.user_id = os.environ['HAB_API_USER']
except KeyError:
    print("User ID must be set by the -u/--user-id option or by setting the environment variable 'HAB_API_USER'")
    sys.exit(1)
try:
    if args.api_token is None:
        args.api_token = os.environ['HAB_API_TOKEN']
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
