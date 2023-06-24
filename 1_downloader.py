import json
from pathlib import Path

import requests


def download_mods():
    with open("mods.json", "rb") as f:
        mods = json.load(f)

    for mod in mods:
        if is_pre4_0(mod):
            url = mod["modfile"]["download"]["binary_url"]

            mod_id_directory_path = Path("1_downloads") / str(mod["id"])

            mod_id_directory_path.mkdir(exist_ok=True)

            mod_file = requests.get(url)
            with open(mod_id_directory_path / mod["modfile"]["filename"], "wb") as f:
                f.write(mod_file.content)


def is_pre4_0(mod):
    return any(tag["name"] == "Pre-Release 4.0" for tag in mod["tags"])


if __name__ == "__main__":
    download_mods()
