import logging
from argparse import ArgumentParser

from k3ng import K3NG, TLE, Satellite


def program_tle_from_file(tle_file: str, ser_port: str, track: bool) -> None:
    rot = K3NG(ser_port)

    with open(tle_file, "r") as file:
        tle_file_data = file.readlines()

    sat_tle = TLE(tle_file_data[0], tle_file_data[1], tle_file_data[2])

    sat = Satellite(0, sat_tle)
    rot.set_time()
    rot.load_tle(sat)
    rot.check_time()
    rot.select_satellite(sat)
    rot.enable_tracking()
    rot.get_tracking_status()


def main():
    parser = ArgumentParser(
        prog="load_and_track.py",
        description="Loads a TLE from a file and begins tracking it",
    )
    parser.add_argument(
        "port",
        help="Serial port connected to an Arduino (typically /dev/ttyACM0)",
    )
    parser.add_argument("tle_file", help="TLE file")

    logging.basicConfig(level=logging.DEBUG)

    args = parser.parse_args()

    program_tle_from_file(args.tle_file, args.port, False)


if __name__ == "__main__":
    main()
