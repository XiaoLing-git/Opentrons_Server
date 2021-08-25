# print("api  __init__")

import os
import platform

_resource_paths = {
        "Linux": ["linux", "discovery"],
        "Darwin": ["mac", "discovery"],
        "Windows": ["windows", "discovery.exe"],
    }
os_system = _resource_paths[platform.system()]

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

PARENT_DIR = os.path.dirname(THIS_DIR)

command_path = os.path.join(\
    os.path.abspath(PARENT_DIR),'Command',os_system[0],os_system[1])
__slots__ = [command_path]
