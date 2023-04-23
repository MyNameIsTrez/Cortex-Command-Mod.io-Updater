import os
import shutil
import signal
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
    mod_directory_path = game_directory_path / "Mods"

    console_log_path = game_directory_path / "LogConsole.txt"
    nothing_special_logged = (
        "- RTE Lua Console -\n"
        "See the Data Realms Wiki for commands: http://www.datarealms.com/wiki/\n"
        "Press F1 for a list of helpful shortcuts\n"
        "-------------------------------------\n"
        "SYSTEM: Activity was reset!\n"
        "ERROR: Finding Scene preset '' failed! Has it been properly defined?\n"
        'SYSTEM: Scene "Fight" was loaded\n'
        'SYSTEM: Activity "Fight" was successfully started'
    )

    for mod_id_folder_path in (
        entry_path
        for entry_path in Path("4_not_boot_logging").iterdir()
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

            # TODO: This may work on Unix, but on Windows,
            # timeout doesn't allow LogConsole.txt to be flushed.
            # try:
            #     completed_process_instance = subprocess.run(
            #         [
            #             game_directory_path / "Cortex Command.debug.release.exe",
            #         ],
            #         cwd=game_directory_path,
            #         timeout=10,
            #     )
            # except subprocess.TimeoutExpired:
            #     pass

            try:
                p = subprocess.Popen(
                    [
                        game_directory_path / "Cortex Command.debug.release.exe",
                    ],
                    cwd=game_directory_path,
                    # start_new_session=True,
                )
                p.wait(timeout=10)
            except subprocess.TimeoutExpired:
                for hwnd in get_hwnds_for_pid(p.pid):
                    print(hwnd, "=>", win32gui.GetWindowText(hwnd))
                    win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                # os.kill(p.pid, signal.SIGHUP)
                # os.kill(p.pid, signal.SIGTERM)
                # os.kill(p.pid, signal.SIGABRT)
                # os.kill(p.pid, signal.SIGINT)
                # p.send_signal(signal.SIGTERM)
                # p.send_signal(signal.CTRL_C_EVENT)
                # p.send_signal(signal.CTRL_BREAK_EVENT)

            # Some sleeping is required for LogConsole.txt to be written back to disk
            # before the .read_text() below is reached.
            time.sleep(1)
            log = console_log_path.read_text()

            if log == nothing_special_logged:
                destination_directory_name = Path("5_not_runtime_logging")
            else:
                destination_directory_name = Path("5_runtime_logging")

            destination_directory_path = (
                destination_directory_name / mod_path.parent.name
            )

            destination_directory_path.mkdir(exist_ok=True)
            shutil.move(mod_in_mods_directory_path, destination_directory_path)

            if log != nothing_special_logged:
                shutil.copy(console_log_path, destination_directory_path)

            shutil.rmtree(mod_path)

            if len(os.listdir(mod_id_folder_path)) == 0:
                mod_id_folder_path.rmdir()


if __name__ == "__main__":
    sort_mods()
