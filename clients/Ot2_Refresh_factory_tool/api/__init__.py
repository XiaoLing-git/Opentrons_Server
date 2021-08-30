print("api  __init__")

import os
import platform
import shutil

_resource_paths = {
        "Linux": ["linux", "discovery"],
        "Darwin": ["mac", "discovery"],
        "Windows": ["windows", "discovery.exe"],
    }
os_system = _resource_paths[platform.system()]

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

PARENT_DIR = os.path.dirname(THIS_DIR)
# print(PARENT_DIR)
command_path = os.path.join(\
    os.path.abspath(PARENT_DIR),'Command','resource_files','discovery',os_system[0],os_system[1])
__slots__ = [command_path]

# shutil.copy(command_path, os.path.join(PARENT_DIR,'dist'))


if __name__ == '__main__':
    shutil.copy(command_path, PARENT_DIR)
