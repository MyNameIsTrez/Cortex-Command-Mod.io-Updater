import shutil
from pathlib import Path


def copy_working():
    game_directory_path = Path("I:/Programming/Cortex-Command-Community-Project")
    mod_directory_path = game_directory_path / "Mods"

    entry_paths = list(Path("5_not_runtime_logging").iterdir())

    index = 0
    for mod_id_folder_path in (
        entry_path for entry_path in entry_paths if entry_path.is_dir()
    ):
        for mod_path in (
            entry_path
            for entry_path in mod_id_folder_path.glob("*")
            if entry_path.suffix == ".rte"
        ):
            # -1 because of .placeholder file
            print(f"{index + 1}/{len(entry_paths) - 1}")
            index += 1

            mod_in_mods_directory_path = mod_directory_path / mod_path.name

            try:
                shutil.copytree(mod_path, mod_in_mods_directory_path)
            except FileExistsError as err:
                print(err)


if __name__ == "__main__":
    copy_working()
