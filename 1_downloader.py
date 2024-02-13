import json
import os
import shutil
from pathlib import Path

import requests


def download_mods():
    with open("mods.json", "rb") as f:
        mods = json.load(f)

    for index, mod in enumerate(mods):
        if is_desired_version(mod):
            # -1 because of .placeholder file
            print(f"{index + 1}/{len(mods) - 1}")

            url = mod["modfile"]["download"]["binary_url"]

            mod_id_directory_path = Path("1_downloads") / str(mod["id"])

            mod_id_directory_path.mkdir(exist_ok=True)

            zip_path = mod_id_directory_path / mod["modfile"]["filename"]

            # TODO: There must be a way to unpack the zip directly,
            # without first writing the zip to disk
            with open(zip_path, "wb") as f:
                mod_file = requests.get(url)
                f.write(mod_file.content)

            shutil.unpack_archive(zip_path, mod_id_directory_path)
            zip_path.unlink()


def is_desired_version(mod):
    return any(tag["name"] == "Pre-Release 5.0" for tag in mod["tags"])


if __name__ == "__main__":
    download_mods()
