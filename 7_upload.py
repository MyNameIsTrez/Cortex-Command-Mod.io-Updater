from pathlib import Path

import modio
import requests


def upload():
    game_id = 508
    api_key = "ab779d10d97eadfb36b43c27ec6292a3"
    mod_id = 1008081

    oauth2 = Path("oauth2.txt").read_text()

    client = modio.Client(api_key=api_key, auth=oauth2)
    game = client.get_game(game_id)
    mod = game.get_mod(mod_id)
    tags = mod.get_tags().results.keys()

    if "Pre-Release 4.0" in tags:
        mod.delete_tags("Pre-Release 4.0")

    if "Pre-Release 5.0" not in tags:
        mod.add_tags("Pre-Release 5.0")

    # new_mod_file = modio.NewModFile(
    #     version="pre5.0-v1.2", changelog="Converted to pre5.0"
    # )
    # mod_zip_path = Path("C:/Users/welfj/Desktop/nrg-pre5.0-v1.2.rte.zip")
    # new_mod_file.add_file(mod_zip_path)
    # # print(new_mod_file)
    # mod.add_file(new_mod_file)

    # for mod_id_folder_path in (
    #     entry_path
    #     for entry_path in Path("5_not_runtime_logging").iterdir()
    #     if entry_path.is_dir()
    # ):
    #     for mod_path in (
    #         entry_path
    #         for entry_path in mod_id_folder_path.glob("*")
    #         if entry_path.suffix == ".rte"
    #     ):
    #         print(mod_path)

    #         return


if __name__ == "__main__":
    upload()
