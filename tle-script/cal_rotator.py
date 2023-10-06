import logging
from argparse import ArgumentParser

from k3ng import K3NG


def calibrate_rotator(ser_port: str) -> None:
    rot = K3NG(ser_port)

    print("To calibrate the antenna, use the rotator box to go to limits")
    input("Please set antenna all the way right (CW) and up")
    rot.cal_full_up()
    rot.cal_full_cw()

    input("Please set antenna all the way left (CCW) and down")
    rot.cal_full_down()
    rot.cal_full_ccw()

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


if __name__ == "__init__":
    main()
