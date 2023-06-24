import os
import shutil
import subprocess
import time
from pathlib import Path

import win32con
import win32gui
import win32process


# Source: http://timgolden.me.uk/python/win32_how_do_i/find-the-window-for-my-subprocess.html
def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def sort_mods():
    game_directory_path = Path("I:/Programming/Cortex-Command-Community-Project-Data")
    # game_directory_path = Path("I:/Games/CCCP Pre5.0")
    mod_directory_path = game_directory_path / "Mods"

    console_log_path = game_directory_path / "LogConsole.txt"
    nothing_special_logged = (
        "- RTE Lua Console -\n"
        "See the Data Realms Wiki for commands: http://www.datarealms.com/wiki/\n"
        "Press F1 for a list of helpful shortcuts\n"
        "-------------------------------------\n"
        "SYSTEM: Activity was reset!\n"
        "ERROR: Finding Scene preset '' failed! Has it been properly defined?\n"
        'SYSTEM: Scene "Benchmark" was loaded\n'
        'SYSTEM: Activity "Combat Benchmark" was successfully started'
    )

    for mod_id_folder_path in (
        entry_path
        for entry_path in Path("5_runtime_logging").iterdir()
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

            # Not sure whether the sleep is necessary, but just in case.
            time.sleep(1)
            # Clear LogConsole.txt, since if the game hard crashes the log isn't flushed,
            # and so the next mods can end up with logs of previous mods.
            console_log_path.open("w").close()

            try:
                p = subprocess.Popen(
                    [
                        game_directory_path / "Cortex Command.exe",
                    ],
                    cwd=game_directory_path,
                )
                p.wait(timeout=60)
            except subprocess.TimeoutExpired:
                for hwnd in get_hwnds_for_pid(p.pid):
                    win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)

            # On Windows at least, some sleeping is required for LogConsole.txt
            # to be written back to disk before the .read_text() below is reached.
            time.sleep(3)
            log = console_log_path.read_text()

            if log == nothing_special_logged:
                destination_directory_name = Path("5_not_runtime_logging")
            else:
                destination_directory_name = Path("5_runtime_logging")

            destination_directory_path = (
                destination_directory_name / mod_path.parent.name
            )

            if log == nothing_special_logged:
                destination_directory_path.mkdir(exist_ok=True)
                shutil.move(mod_in_mods_directory_path, destination_directory_path)

                shutil.rmtree(mod_path)

                if len(os.listdir(mod_id_folder_path)) == 1:
                    os.remove(mod_id_folder_path / "LogConsole.txt")

                if len(os.listdir(mod_id_folder_path)) == 0:
                    mod_id_folder_path.rmdir()
            else:
                shutil.copy(console_log_path, destination_directory_path)

                # TODO: Unify this line with whatever happens in the true case above.
                shutil.rmtree(mod_in_mods_directory_path)
                return


if __name__ == "__main__":
    sort_mods()
