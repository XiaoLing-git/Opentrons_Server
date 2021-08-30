import os
import sys
PARENT_DIR = os.path.abspath(os.path.join(os.getcwd(),'.'))
sys.path.append(PARENT_DIR)
# print(PARENT_DIR)

from api import robot_api
from api.interactive import interactive_shell


import os


def main()->None:
    with robot_api.find() as robot:
        print(f"SSHing into {robot.hostname_or_ip}...")
        interactive_shell(robot.start_shell())


if __name__ == '__main__':

    DIST_DIR = PARENT_DIR
    print(DIST_DIR)
    res = os.environ["Path"]
    os.environ["Path"] = res + DIST_DIR +";"
    main()