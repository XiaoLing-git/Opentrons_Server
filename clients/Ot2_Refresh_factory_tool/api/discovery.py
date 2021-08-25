import subprocess

from . import command_path


class NoRobotFoundError(RuntimeError):
    pass


def get_executable()->str:
    return command_path


def find(ip_prefix:str="") -> str:
    cmd = get_executable()
    res = subprocess.run([cmd,'find','-i',ip_prefix],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         encoding='utf-8',)
    lines = [line for line in res.stdout.split("\n") if line.strip()]
    if not lines or lines[-1].startswith("Timed out"):
        raise NoRobotFoundError()
    return lines[-1].strip()


# if __name__ == '__main__':
#     res= find()
#     print(res)
