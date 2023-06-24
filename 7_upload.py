import json
import shutil
import tempfile
import time
from pathlib import Path

import modio


def get_mods_tags(mods):
    mods_tags = {}

    for mod in mods:
        id_ = mod["id"]
        tags = mod["tags"]
        mods_tags[id_] = [tag["name"] for tag in tags]

    return mods_tags


def upload():
    game_id = 508
    api_key = "ab779d10d97eadfb36b43c27ec6292a3"

    with open("mods.json", "rb") as f:
        mods = json.load(f)
    mods_tags = get_mods_tags(mods)

    oauth2 = Path("oauth2.txt").read_text()

    client = modio.Client(api_key=api_key, access_token=oauth2)
    game = client.get_game(game_id)

    for mod_id_folder_path in (
        entry_path
        for entry_path in Path("5_not_runtime_logging").iterdir()
        if entry_path.is_dir()
    ):
        print(mod_id_folder_path)

        mod_id = int(mod_id_folder_path.name)

        tags = mods_tags[mod_id]

        print("Getting the mod...")
        mod = game.get_mod(mod_id)

        if "Pre-Release 4.0" in tags:
            print("Deleting old tag...")
            mod.delete_tags("Pre-Release 4.0")

            if "Pre-Release 5.0" not in tags:
                print("Adding new tag...")
                mod.add_tags("Pre-Release 5.0")

            print("Creating a temporary directory...")
            tmp_dir = Path(tempfile.mkdtemp())

            try:
                print("Zipping...")
                shutil.make_archive(
                    base_name=tmp_dir / f"{mod.name_id}.rte",
                    format="zip",
                    root_dir=Path("5_not_runtime_logging") / str(mod_id),
                )

                print("Creating the mod.io Python zip file...")
                new_mod_file = modio.NewModFile(
                    version="pre5.0-v1.0", changelog="Converted to pre5.0"
                )
                mod_zip_path = tmp_dir / f"{mod.name_id}.rte.zip"
                new_mod_file.add_file(mod_zip_path)

                print("Adding the file...")
                mod.add_file(new_mod_file)

                print("Sorting the zip...")
                shutil.move(
                    mod_id_folder_path,
                    Path("7_uploaded") / mod_id_folder_path.name,
                )

            finally:
                print("Removing the temporary directory...")
                shutil.rmtree(tmp_dir)

            time.sleep(10)
        else:
            print("Skipping this mod, since it doesn't have the 'Pre-Release 4.0' tag")
            shutil.move(
                mod_id_folder_path,
                Path("7_skipped") / mod_id_folder_path.name,
            )


if __name__ == "__main__":
    upload()
