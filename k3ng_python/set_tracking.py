import logging
from argparse import ArgumentParser

from k3ng_python import K3NG


def toggle_tracking(rot: K3NG) -> None:
    rot.get_trackable()
    if "TRACKING ENABLED" in rot.get_tracking_status():
        rot.disable_tracking()
    else:
        rot.enable_tracking()


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = ArgumentParser(
        prog="set_tracking.py", description="Set state of satellite tracking"
    )

    parser.add_argument(
        "port", help="Serial port connected to an Arduino (typically /dev/ttyACM0)"
    )

    parser.add_argument(
        "state",
        help="State of tracking (on | off | [toggle])",
        nargs="?",
        default="toggle",
    )

    args = parser.parse_args()

    rot = K3NG(args.port)

    if args.state == "on":
        rot.enable_tracking()
    elif args.state == "off":
        rot.disable_tracking()
    else:
        toggle_tracking(
            rot,
        )


if __name__ == "__main__":
    main()
