from api import robot_api

import os
import time
import pathlib


def _generate_remote_dir() -> pathlib.PurePosixPath:
    unique_suffix = "-" + time.strftime("%Y_%m_%d_%H_%I_%S",\
                                        time.localtime(time.time()))
    directory_name = "opentrons-factory-tools" + unique_suffix
    return pathlib.PurePosixPath("/tmp") / directory_name


def _install_and_run_factory_tool(robot: robot_api.RobotApi):
    local_wheel_path = ""
    local_wheel = os.path.dirname(local_wheel_path)
    remote_dir = _generate_remote_dir()
    remote_wheel_path = remote_dir / local_wheel
    robot.run_ssh_command("mkdir -p {}".format(remote_dir))



if __name__ == '__main__':
    res = _generate_remote_dir()
    print(res)
    # with robot_api.find() as robot:
    #     _install_and_run_factory_tool(robot)