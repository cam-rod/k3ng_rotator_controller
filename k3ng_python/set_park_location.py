import logging
from argparse import ArgumentParser

from k3ng import K3NG


def calibrate_rotator(ser_port: str) -> None:
    rot = K3NG(ser_port)

    az = rot.get_azimuth()
    el = rot.get_elevation()

    input(f"Setting park to ({az}, {el}). Are you sure?")

    rot.set_park_location(int(az), int(el))
    rot.save_to_eeprom()


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser(
        prog="set_park_location",
        description="Sets current location to park location, and save it",
    )

    parser.add_argument(
        "port", help="Serial port connected to an Arduino (typically /dev/ttyACM0)"
    )

    args = parser.parse_args()

    calibrate_rotator(args.port)


if __name__ == "__main__":
    main()
