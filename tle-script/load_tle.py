from argparse import ArgumentParser

from k3ng import K3NG, Satellite


def program_tle(sat_id: int, ser_port: str) -> None:
    rot = K3NG(ser_port)

    sat = Satellite(sat_id)
    rot.load_tle(sat)


def main():
    parser = ArgumentParser(
        prog="load_tle.py",
        description="Acquires a two-line element set (TLE) from a given satellite on SatNOGS, and loads it onto a "
        "connected Arduino running K3NG. Can be run as a cron script or otherwise.",
    )
    parser.add_argument(
        "norad_id",
        type=int,
        help="NORAD ID of a satellite, (ex. use 25544 for the ISS)",
    )
    parser.add_argument(
        "port",
        help="Serial port connected to an Arduino (typically /dev/ttyACM0)",
    )

    args = parser.parse_args()

    program_tle(args.norad_id, args.port)


if __name__ == "__main__":
    main()
