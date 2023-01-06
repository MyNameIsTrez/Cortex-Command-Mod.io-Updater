import mod_converter
import mod_downloader
import mod_sorter


def main():
    mod_downloader.download_mods()
    mod_converter.convert_mods()
    mod_sorter.sort_mods()


if __name__ == "__main__":
    main()
