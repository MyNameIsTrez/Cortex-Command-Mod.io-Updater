import shutil
import tempfile
from pathlib import Path

import modio


def upload():
    game_id = 508
    api_key = "ab779d10d97eadfb36b43c27ec6292a3"
    mod_id = 1008081  # new boston revolutionary guard
    # mod_id = 173180  # gwtb

    oauth2 = Path("oauth2.txt").read_text()

    client = modio.Client(api_key=api_key, auth=oauth2)
    game = client.get_game(game_id)
    mod = game.get_mod(mod_id)
    # print(mod.name)
    tags = mod.get_tags().results.keys()

    # TODO: Only upload if the mod still has the old "Pre-Release 4.0" tag

    # TODO: Make sure the pre5 mods have the correct version of "Pre-Release 5.0" before uploading

    # TODO: Create zip in tmp directory, or tmp filestream

    if "Pre-Release 4.0" in tags:
        mod.delete_tags("Pre-Release 4.0")

        if "Pre-Release 5.0" not in tags:
            mod.add_tags("Pre-Release 5.0")

        tmp_dir = Path(tempfile.mkdtemp())
        try:
            shutil.make_archive(
                base_name=tmp_dir / f"{mod.name_id}.rte",
                format="zip",
                root_dir=Path("5_not_runtime_logging") / str(mod_id),
            )

            new_mod_file = modio.NewModFile(
                version="pre5.0-v1.0", changelog="Converted to pre5.0"
            )
            mod_zip_path = tmp_dir / f"{mod.name_id}.rte.zip"
            new_mod_file.add_file(mod_zip_path)
            # print(new_mod_file)

            mod.add_file(new_mod_file)

        finally:
            shutil.rmtree(tmp_dir)
    else:
        print("Skipping this mod, since it doesn't have the 'Pre-Release 4.0' tag")

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
