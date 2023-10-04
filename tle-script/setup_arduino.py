from argparse import ArgumentParser
from datetime import datetime, timedelta, timezone
from typing import Final

import maidenhead
from serial import Serial

from load_tle import configure_port, restore_port

ARD_LINESEP: Final[bytes] = b"\r"


def load_config(grid_square: str, port: str) -> None:
    port_path, modified_perms = configure_port(port)
    with Serial(str(port_path), 9600, timeout=2, inter_byte_timeout=0.5) as arduino:
        print("Flushing leftover data...")
        arduino.write(ARD_LINESEP)
        arduino.flush()
        arduino.reset_output_buffer()

        print(f"Setting grid square{grid_square}... ", end="")
        arduino.write(b"\\G" + grid_square.encode("ascii") + ARD_LINESEP)
        arduino.flush()
        arduino.reset_output_buffer()

        result = arduino.read(1000)
        if grid_square.encode("ascii") not in result:
            print(
                "ERROR: Grid square was not found in the output.\n===RECORDED OUTPUT==="
            )
            print(result)
            print("===END OF OUTPUT===")
            restore_port(port_path, modified_perms)
            return
        else:
            print("Confirmed")
        arduino.reset_input_buffer()
        arduino.reset_output_buffer()

        print(f"Setting time... ", end="")
        current_time = datetime.now(tz=timezone.utc)
        arduino.write(b"\\O" + current_time.strftime("%Y%m%d%H%M%S").encode("ascii"))
        arduino.flush()
        arduino.reset_input_buffer()
        arduino.reset_output_buffer()

        arduino.write(b"\\C")
        result = datetime.fromisoformat(arduino.read(1000).decode("ascii"))
        if abs(result - current_time) < timedelta(seconds=10):
            print(f"Set to {result.isoformat()}")
        else:
            print(
                "ERROR: offset between set and returned time is greater than 10 seconds"
            )
            print(
                f"Inputted time: {current_time.isoformat()}\nValue of '\\C': {result.isoformat()}"
            )

    restore_port(port_path, modified_perms)


def main():
    parser = ArgumentParser(
        description="Configures current time and location for the K3NG software."
    )
    parser.add_argument(
        "port",
        help="Serial port connected to an Arduino; do not include `/dev/` from the path (typically ttyACM0)",
    )
    location = parser.add_mutually_exclusive_group(required=True)
    location.add_argument(
        "--coords",
        "-c",
        nargs=2,
        metavar=("LAT", "LON"),
        type=float,
        help="Coordinates of the antenna, using decimal degrees (ex. 48.235 -112.237)",
    )
    location.add_argument(
        "--grid-square",
        "-g",
        metavar="MAIDENHEAD",
        help="Maidenhead grid at subsquare precision/3 pairs (ex. FN03hp)",
    )
    args = parser.parse_args()

    grid_square = (
        maidenhead.to_maiden(args.coords[0], args.coords[1])
        if args.coords
        else args.grid_square
    )
    load_config(grid_square, args.port)


if __name__ == "__main__":
    main()
