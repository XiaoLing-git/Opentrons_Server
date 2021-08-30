"""The implementation of the opentrons_cleanup command."""

from clients.Ot2_Refresh_factory_tool.api import robot_api


def main() -> None:  # noqa: D103

    print("Finding robot...")
    try:
        robot = robot_api.find()
    except Exception:
        raise
    try:
        with robot:
            robot.remove_all_pubkeys()
    except Exception:
        raise
    else:
        print("OK")


if __name__ == '__main__':
    main()