from api import robot_api
from api.interactive import interactive_shell


def main()->None:
    with robot_api.find() as robot:
        print(f"SSHing into {robot.hostname_or_ip}...")
        interactive_shell(robot.start_shell())


if __name__ == '__main__':
    main()