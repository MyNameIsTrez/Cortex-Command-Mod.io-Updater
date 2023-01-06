from pathlib import Path


def sort_mods():
    for mod_path in get_mod_paths():
        # print(mod_path)
        converted_path = (
            Path(mod_path).parent.parent / "converted" / Path(mod_path).name
        )
        print(converted_path)

        mod_converter.convert(mod_path, converted_path)


def get_mod_paths():
    for entry in Path("downloads").iterdir():
        # TODO: Consider allowing .rar and other compression formats
        if entry.suffix == ".zip":
            yield entry.resolve()


if __name__ == "__main__":
    sort_mods()
