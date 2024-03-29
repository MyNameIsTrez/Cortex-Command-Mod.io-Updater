import os
import shutil
import subprocess
from pathlib import Path


def sort_mods():
    game_directory_path = Path("I:/Programming/Cortex-Command-Community-Project")
    mod_directory_path = game_directory_path / "Mods"

    console_log_path = game_directory_path / "LogConsole.txt"
    nothing_special_logged = (
        "- RTE Lua Console -\n"
        "See the Data Realms Wiki for commands: http://www.datarealms.com/wiki/\n"
        "Press F1 for a list of helpful shortcuts\n"
        "-------------------------------------"
    )

    entry_paths = list(Path("4_boot_logging").iterdir())

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

            print(mod_path)

            mod_in_mods_directory_path = mod_directory_path / mod_path.name

            shutil.copytree(mod_path, mod_in_mods_directory_path)

            completed_process_instance = subprocess.run(
                [
                    game_directory_path / "Cortex Command.exe",
                    # "-ext-validate",
                ],
                cwd=game_directory_path,
            )

            log = console_log_path.read_text()

            if (
                log == nothing_special_logged
                and completed_process_instance.returncode == 0
            ):
                destination_directory_name = Path("4_not_boot_logging")

                destination_directory_path = (
                    destination_directory_name / mod_path.parent.name
                )
                # print(destination_directory_path)
                destination_directory_path.mkdir(exist_ok=True)
                shutil.move(mod_in_mods_directory_path, destination_directory_path)

                shutil.rmtree(mod_path)

                if len(os.listdir(mod_id_folder_path)) == 0:
                    mod_id_folder_path.rmdir()
            else:
                # TODO: Unify this line with whatever happens in the true case above.
                shutil.rmtree(mod_in_mods_directory_path)
                return


if __name__ == "__main__":
    sort_mods()
