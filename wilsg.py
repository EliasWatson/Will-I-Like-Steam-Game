import requests
import json

import config # You need to make config.py in this directory with the API_KEY variable set to your Steam API Key

review_url = "https://store.steampowered.com/appreviews/%d?json=1&review_type=positive&purchase_type=steam&start_offset=%d"
playtime_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%d&include_played_free_games=1&include_appinfo=1&format=json"

def get_review_user_ids(app_id, amount):
    user_ids = []
    offset = 0

    while len(user_ids) < amount:
        r = requests.get(review_url % (app_id, offset))
        data = json.loads(r.text)

        for review in data["reviews"]:
            user_ids.append(review["author"]["steamid"])
            if len(user_ids) == amount:
                return user_ids

        offset = offset + 20

    return user_ids

def get_game_playtime_user(user_id):
    r = requests.get(playtime_url % (config.API_KEY, user_id))
    data = json.loads(r.text)

    playtime = {}
    for g in data["response"]["games"]:
        playtime[g["name"]] = g["playtime_forever"]

    return playtime

playtime = get_game_playtime_user(76561198097022834)
for i,v in enumerate(playtime):
    print "%s - %s" % (v, playtime[v])
