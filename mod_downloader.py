# import json
import time
from pathlib import Path

import requests


def download_mods():
    game_id = 508
    api_key = "ab779d10d97eadfb36b43c27ec6292a3"
    mods_per_request = 100

    headers = {"Accept": "application/json"}

    mod_offset = 0
    while True:
        response = requests.get(
            f"https://api.mod.io/v1/games/{game_id}/mods?_limit={mods_per_request}&_offset={mod_offset}",
            params={"api_key": api_key},
            headers=headers,
        ).json()

        # with open("lol.json", "w", encoding="utf-8") as f:
        #     json.dump(response, f, ensure_ascii=False, indent=4)

        for mod in response["data"]:
            if is_pre4_0(mod):
                url = mod["modfile"]["download"]["binary_url"]

                mod_id_directory_path = Path("downloads") / str(mod["id"])

                mod_id_directory_path.mkdir(exist_ok=True)

                mod_file = requests.get(url)
                with open(
                    mod_id_directory_path / mod["modfile"]["filename"], "wb"
                ) as f:
                    f.write(mod_file.content)

        mod_offset += mods_per_request

        if response["result_count"] < mods_per_request:
            break

        time.sleep(5)


def is_pre4_0(mod):
    return any(tag["name"] == "Pre-Release 4.0" for tag in mod["tags"])


if __name__ == "__main__":
    download_mods()
