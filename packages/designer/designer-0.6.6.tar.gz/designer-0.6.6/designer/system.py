import sys


def running_on_windows() -> bool:
    return sys.platform == "win32"


def running_on_mac_os() -> bool:
    return sys.platform == "darwin"


def running_on_linux() -> bool:
    return sys.platform == "linux"


def running_on_skulpt() -> bool:
    return sys.platform == 'skulpt'


def setup_debug_mode():
    if running_on_mac_os():
        try:
            import tkinter as tk
            root = tk.Tk()
            root.update()
            root.destroy()
        except:
            pass
