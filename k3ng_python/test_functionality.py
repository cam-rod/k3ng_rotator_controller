import logging
from argparse import ArgumentParser

from k3ng import K3NG


def test_function(ser_port: str) -> None:
    rot = K3NG(ser_port)
    input("Set rotator to fully down, fully left. Enter to continue")

    rot.up()
    input("Moving UP. Enter to continue.")

    rot.stop()
    rot.right()
    input("Moving RIGHT. Enter to continue.")

    rot.stop()
    rot.set_elevation(0)
    rot.set_azimuth(0)

    input("Going home (0, 0). Enter to continue")
    print("Done!")


def main():
    parser = ArgumentParser(
        prog="test_functionality",
        description="Tests all four motion channels on the rotator",
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
