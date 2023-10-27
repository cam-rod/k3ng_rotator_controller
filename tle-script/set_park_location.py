import logging
from argparse import ArgumentParser

from k3ng import K3NG


def calibrate_rotator(ser_port: str) -> None:
    rot = K3NG(ser_port)

    rot.get_park_location()

    print("Position antenna to parked location")
    input("Press any key when positioned")
    az = rot.get_azimuth()
    el = rot.get_elevation()

    rot.set_park_location(int(az), int(el))
    rot.save_to_eeprom()


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
