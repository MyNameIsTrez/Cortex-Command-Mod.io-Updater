import os
import shutil
import subprocess
from pathlib import Path


def convert_mods():
    converter_dir_path = Path("I:/Programming/Cortex-Command-Mod-Converter-Engine/")
    converter_path = converter_dir_path / "Cortex-Command-Mod-Converter-Engine.exe"

    output_folder_path = Path("2_converted").resolve()

    entry_paths = list(Path("1_downloads").iterdir())

    index = 0
    for mod_id_folder_path in (
        entry_path for entry_path in entry_paths if entry_path.is_dir()
    ):
        # -1 because of .placeholder file
        print(f"{index + 1}/{len(entry_paths) - 1}")
        index += 1

        mod_output_folder_path = output_folder_path / mod_id_folder_path.name
        print(mod_output_folder_path)

        mod_output_folder_path.mkdir(exist_ok=True)

        for mod_path in (
            entry_path
            for entry_path in mod_id_folder_path.glob("*")
            if entry_path.suffix == ".rte"
        ):
            completed_process_instance = subprocess.run(
                [
                    converter_path,
                    mod_path.resolve(),
                    mod_output_folder_path / mod_path.name,
                ],
                cwd=converter_dir_path,
            )
            # print(completed_process_instance)
            assert completed_process_instance.returncode == 0

            # TODO: Remove the input folder, if conversion succeeded
            shutil.rmtree(mod_path)

            if len(os.listdir(mod_id_folder_path)) == 0:
                mod_id_folder_path.rmdir()


if __name__ == "__main__":
    convert_mods()
