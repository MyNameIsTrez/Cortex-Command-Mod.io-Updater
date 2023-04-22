import os
import shutil
from pathlib import Path

from cortex_command_mod_converter_engine import convert


def convert_mods():
    # TODO: Try to remove .resolve() here
    output_folder_path = Path("2_converted").resolve()

    extensions = {".zip", ".rte"}

    for mod_id_folder_path in (
        entry_path
        for entry_path in Path("1_downloads").iterdir()
        if entry_path.is_dir()
    ):
        mod_output_folder_path = output_folder_path / mod_id_folder_path.name

        print(mod_output_folder_path)

        mod_output_folder_path.mkdir(exist_ok=True)

        for mod_path in (
            entry_path
            for entry_path in mod_id_folder_path.glob("*")
            if entry_path.suffix in extensions
        ):
            convert.convert(
                mod_path, mod_output_folder_path, remove_input_mod_path=True
            )
            if len(os.listdir(mod_id_folder_path)) == 0:
                mod_id_folder_path.rmdir()


if __name__ == "__main__":
    convert_mods()
