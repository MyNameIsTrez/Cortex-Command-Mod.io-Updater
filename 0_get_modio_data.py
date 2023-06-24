import json
import time

import requests


def get_modio_data():
    game_id = 508
    api_key = "ab779d10d97eadfb36b43c27ec6292a3"
    mods_per_request = 100

    headers = {"Accept": "application/json"}

    data = []

    mod_offset = 0
    while True:
        response = requests.get(
            f"https://api.mod.io/v1/games/{game_id}/mods?_limit={mods_per_request}&_offset={mod_offset}",
            params={"api_key": api_key},
            headers=headers,
        ).json()

        data += response["data"]

        mod_offset += mods_per_request

        if response["result_count"] < mods_per_request:
            break

        time.sleep(5)

    with open(f"mods.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_modio_data()
