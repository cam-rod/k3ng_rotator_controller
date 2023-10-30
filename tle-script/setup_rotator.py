import logging
from argparse import ArgumentParser

from k3ng import K3NG


def default_config(ser_port: str, location: str) -> None:
    rot = K3NG(ser_port)
    rot.set_loc(location)
    rot.set_time()

    print("Success!")


def main():
    parser = ArgumentParser(
        prog="setup_rotator.py", description="Sets location and time of the rotator"
    )
    parser.add_argument(
        "port",
        help="Serial port connected to an Arduino (typically /dev/ttyACM0)",
    )
    parser.add_argument(
        "location",
        type=str,
        help="Maidenhead grid location of groundstation at subgrid precision",
        default="FN03hp",
        nargs="?",
    )

    logging.basicConfig(level=logging.DEBUG)
    args = parser.parse_args()

    default_config(args.port, args.location)


if __name__ == "__main__":
    main()
