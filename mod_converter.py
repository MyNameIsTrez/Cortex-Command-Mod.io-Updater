from pathlib import Path

from cortex_command_mod_converter_engine import convert


def convert_mods():
    output_folder_path = Path("converted").resolve()

    extensions = (".zip", ".rte")

    for mod_path in (x for x in Path("downloads").glob("*") if x.suffix in extensions):
        convert.convert(
            mod_path,
            output_folder_path,
            remove_input_mod_folder=False,
        )


if __name__ == "__main__":
    convert_mods()
