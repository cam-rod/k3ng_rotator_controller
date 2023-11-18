import logging
from argparse import ArgumentParser

from k3ng import K3NG


def calibrate_rotator(ser_port: str) -> None:
    rot = K3NG(ser_port)

    print(f"Sending antenna to {rot.get_park_location()}")

    rot.park()


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser(
        prog="park_ant", description="Sends antenna to park location"
    )

    parser.add_argument(
        "port", help="Serial port connected to an Arduino (typically /dev/ttyACM0)"
    )

    args = parser.parse_args()

    calibrate_rotator(args.port)


if __name__ == "__main__":
    main()
