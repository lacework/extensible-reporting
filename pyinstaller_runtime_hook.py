# pyinstaller_runtime_hook.py

import ctypes.util

_original_find_library = ctypes.util.find_library

def patched_find_library(name):
    # For Windows system libraries loaded via ctypes,
    # simply return the name (they’re provided by the OS).
    if name.lower() in ("user32", "msvcrt"):
        return name
    return _original_find_library(name)

ctypes.util.find_library = patched_find_library

