import shutil
from pathlib import Path


def copy_working():
    game_directory_path = Path("I:/Programming/Cortex-Command-Community-Project-Data")
    # game_directory_path = Path("I:/Games/CCCP Pre5.0")
    mod_directory_path = game_directory_path / "Mods"

    for mod_id_folder_path in (
        entry_path
        for entry_path in Path("5_not_runtime_logging").iterdir()
        if entry_path.is_dir()
    ):
        for mod_path in (
            entry_path
            for entry_path in mod_id_folder_path.glob("*")
            if entry_path.suffix == ".rte"
        ):
            mod_in_mods_directory_path = mod_directory_path / mod_path.name

            try:
                shutil.copytree(mod_path, mod_in_mods_directory_path)
            except FileExistsError as err:
                print(err)


if __name__ == "__main__":
    copy_working()
