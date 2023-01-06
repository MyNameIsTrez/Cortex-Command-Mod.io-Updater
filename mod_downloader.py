import requests, time


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

        for mod in response["data"]:
            if is_pre4_0(mod):
                url = mod["modfile"]["download"]["binary_url"]
                mod_file = requests.get(url)
                with open(f"downloads/{mod['name']}.zip", "wb") as f:
                    f.write(mod_file.content)

        mod_offset += mods_per_request

        if response["result_count"] < mods_per_request:
            break

        time.sleep(5)


def is_pre4_0(mod):
    return any(tag["name"] == "Pre-Release 4.0" for tag in mod["tags"])


if __name__ == "__main__":
    download_mods()
