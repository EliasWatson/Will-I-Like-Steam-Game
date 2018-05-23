import requests
import json

import config # You need to make config.py in this directory with the API_KEY variable set to your Steam API Key

review_url = "https://store.steampowered.com/appreviews/%d?json=1&review_type=positive&purchase_type=steam&start_offset=%d"
playtime_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&include_played_free_games=1&include_appinfo=1&format=json"

def get_review_user_ids(app_id, amount):
    user_ids = []
    offset = 0

    while len(user_ids) < amount:
        r = requests.get(review_url % (app_id, offset))
        data = json.loads(r.text)

        for review in data["reviews"]:
            user_ids.append(review["author"]["steamid"].encode('utf-8').strip())
            if len(user_ids) == amount:
                return user_ids

        offset = offset + 20

    return user_ids

def get_game_playtime_user(user_id):
    r = requests.get(playtime_url % (config.API_KEY, user_id))
    data = json.loads(r.text)

    if "games" not in data["response"]:
        return {}

    playtime = {}
    for g in data["response"]["games"]:
        if g["playtime_forever"] > 0:
            playtime[g["name"].encode('utf-8').strip()] = g["playtime_forever"]

    return playtime

def get_game_playtime_user_list(user_ids):
    playtime = {}
    for user_id in user_ids:
        user_playtime = get_game_playtime_user(user_id)
        playtime = { k: playtime.get(k, 0) + user_playtime.get(k, 0) for k in set(playtime) | set(user_playtime) }
    return playtime

playtime = get_game_playtime_user_list(get_review_user_ids(435150, 20))
for key, value in sorted(playtime.iteritems(), key=lambda (k,v): (v,k)):
    print "%s - %s" % (value, key)
