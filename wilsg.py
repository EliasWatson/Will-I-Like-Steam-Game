import requests
import json

review_url = "https://store.steampowered.com/appreviews/%d?json=1&review_type=positive&purchase_type=steam&start_offset=%d"

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

print len(get_review_user_ids(435150, 30))
