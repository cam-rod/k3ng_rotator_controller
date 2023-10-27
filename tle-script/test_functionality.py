import logging
from argparse import ArgumentParser

from k3ng import K3NG, Satellite


def test_function(ser_port: str) -> None:

    rot = K3NG(ser_port)
    input("Set rotator to fully down, fully left. Enter to continue")

    rot.up()
    input("Moving UP. Enter to continue.")

    rot.stop()
    rot.down()
    input("Moving DOWN. Enter to continue.")

    rot.stop()
    rot.right()
    input("Moving RIGHT. Enter to continue.")

    rot.stop()
    rot.left()
    input("Moving LEFT. Enter to continue.")

    rot.stop()
    rot.set_elevation(0)
    rot.set_azimuth(0)

    input("Going home (0, 0). Enter to continue")
    print("Done!")


def main():
    parser = ArgumentParser(
        prog="load_and_track.py",
        description="Loads a TLE and begins tracking it"
    )
    parser.add_argument(
        "port",
        help="Serial port connected to an Arduino (typically /dev/ttyACM0)",
    )

    logging.basicConfig(level=logging.INFO)

    args = parser.parse_args()

    test_function(args.port)


if __name__ == "__main__":
    main()
