import os
import shutil
import subprocess
from pathlib import Path


def sort_mods():
    game_directory_path = Path("I:/Programming/Cortex-Command-Community-Project-Data")
    mod_directory_path = game_directory_path / "Mods"

    for mod_id_folder_path in (
        entry_path
        for entry_path in Path("2_converted").iterdir()
        if entry_path.is_dir()
    ):
        for mod_path in (
            entry_path
            for entry_path in mod_id_folder_path.glob("*")
            if entry_path.suffix == ".rte"
        ):
            print(mod_path)

            mod_in_mods_directory_path = mod_directory_path / mod_path.name

            shutil.copytree(mod_path, mod_in_mods_directory_path)

            # print(mod_in_mods_directory_path)

            completed_process_instance = subprocess.run(
                [
                    game_directory_path / "Cortex Command.debug.release.exe",
                    "-ext-validate",
                ],
                cwd=game_directory_path,
            )
            print(completed_process_instance)

            if completed_process_instance.returncode == 0:
                destination_directory_name = Path("3_not_boot_crashing")
            else:
                destination_directory_name = Path("3_boot_crashing")

            destination_directory_path = (
                destination_directory_name / mod_path.parent.name
            )
            # print(destination_directory_path)
            destination_directory_path.mkdir(exist_ok=True)
            shutil.move(mod_in_mods_directory_path, destination_directory_path)

            shutil.rmtree(mod_path)

            if len(os.listdir(mod_id_folder_path)) == 0:
                mod_id_folder_path.rmdir()


if __name__ == "__main__":
    sort_mods()