"""Build standalone executable files for the current platform."""

# todo(mm, 2021-02-05): Now that we have a project-wide Makefile, this logic
# could live there and we could delete this script.
import os
import pathlib
import typing

from PyInstaller.__main__ import run as run_pyinstaller
from api import PARENT_DIR, command_path
import shutil


WRAPPER_DIR = pathlib.Path("main")



def _freeze_all() -> None:
    for script in _get_scripts():
        print(f"Generating standalone executable from {script}...")
        _freeze(script)


def _freeze(script: pathlib.Path) -> None:
    """Use PyInstaller to *freeze* the given .py script.

    The output, a standalone executable file, will be placed in dist/. Its name
    will be based on the given .py script.
    """
    # fmt: off
    run_pyinstaller([
        "--log-level", "WARN",  # INFO by default, which is noisy.
        "--onefile",
        "--additional-hooks-dir", "pyinstaller_hooks",
        str(script)
    ])
    # fmt: on


def _get_scripts() -> typing.Iterable[pathlib.Path]:
    return WRAPPER_DIR.glob("*.py")


if __name__ == "__main__":
    this_dir = os.path.dirname(__file__)
    _freeze_all()
    shutil.copy(command_path, os.path.join(PARENT_DIR, 'dist'))

