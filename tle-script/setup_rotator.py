import logging
from argparse import ArgumentParser

from k3ng import K3NG


def default_config(ser_port: str, location: str) -> None:
    rot = K3NG(ser_port)
    rot.set_loc(location)
    rot.set_time()


def main():
    parser = ArgumentParser(
        prog="load_tle.py",
        description="Acquires a two-line element set (TLE) from a given satellite on SatNOGS, and loads it onto a "
        "connected Arduino running K3NG. Can be run as a cron script or otherwise.",
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
