import logging
from argparse import ArgumentParser

from k3ng import K3NG


def calibrate_rotator(ser_port: str) -> None:
    rot = K3NG(ser_port)

    rot.park()


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser(
        prog="cal_rotator.py", description="Assists with calibration of the antenna"
    )

    parser.add_argument(
        "port", help="Serial port connected to an Arduino (typically /dev/ttyACM0)"
    )

    args = parser.parse_args()

    calibrate_rotator(args.port)


if __name__ == "__main__":
    main()
