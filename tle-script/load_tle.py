from argparse import ArgumentParser
import os
from pathlib import Path
import stat
import sys
from typing import cast, Final, TypedDict

import serial
import requests

ARD_LINESEP: Final[bytes] = b"\r"


class TLE(TypedDict):
    tle0: str
    tle1: str
    tle2: str
    tle_source: str
    sat_id: str
    norad_cat_id: int
    updated: str


def retrieve_tle(norad_id: int) -> TLE:
    params = {"format": "json", "norad_cat_id": str(norad_id)}
    resp: requests.Response = requests.get(
        f"https://db.satnogs.org/api/tle/", params=params
    )
    return cast(TLE, resp.json()[0])


def configure_port(port: str) -> (Path, bool):
    modified_perms = False
    port_path = Path("/dev") / port
    if not port_path.exists():
        raise FileNotFoundError(port_path)

    if not os.access(
        port_path,
        os.R_OK | os.W_OK,
        effective_ids=(os.access in os.supports_effective_ids),
    ):
        # Attempt to chmod file
        if os.geteuid() != 0:
            print(
                f"Unable to acquire read/write permissions on {port_path}.\n"
                + "Please change permissions, or run this script as superuser."
            )
            sys.exit(1)

        print(f"Changing permissions on {port_path}")
        curr_mode: int = stat.S_IMODE(os.stat(port_path).st_mode)
        os.chmod(port_path, curr_mode | stat.S_IROTH | stat.S_IWOTH)
        modified_perms = True

    return port_path, modified_perms


def restore_port(port_path: Path, modified_perms: bool) -> None:
    if modified_perms:
        print(f"Restoring permissions on {port_path}")
        curr_mode: int = stat.S_IMODE(os.stat(port_path).st_mode)
        os.chmod(port_path, curr_mode & ~stat.S_IROTH & ~stat.S_IWOTH)


# Derived from https://blog.mbedded.ninja/programming/operating-systems/linux/linux-serial-ports-using-c-cpp/
def program_tle(tle: TLE, port: str) -> None:
    port_path, modified_perms = configure_port(port)
    sat_name = tle["tle0"].encode("ascii")

    with serial.Serial(
        str(port_path), 9600, timeout=2, inter_byte_timeout=0.5
    ) as arduino:
        print("Flushing leftover data...")
        arduino.write(ARD_LINESEP)
        arduino.flush()
        arduino.reset_output_buffer()

        print("Writing TLE...")
        arduino.write(b"\\#" + ARD_LINESEP)
        arduino.write(sat_name + ARD_LINESEP)
        arduino.write(tle["tle1"].encode("ascii") + ARD_LINESEP)
        arduino.write(tle["tle2"].encode("ascii") + ARD_LINESEP)
        arduino.write(ARD_LINESEP)
        arduino.flush()
        arduino.reset_output_buffer()

        # Confirm TLE saved
        result = arduino.read(1000)
        if b"TLE corrupt" in result:
            print("ERROR: TLE was corrupted.\n===START OF TLE===")
            print(tle)
            print("===END OF TLE===")
            print(result)
            restore_port(port_path, modified_perms)
            return port_path
        if b"File was truncated" in result:
            print("ERROR: File was truncated due to lack of EEPROM storage.")
            restore_port(port_path, modified_perms)
            return port_path
        if sat_name not in result:
            print("ERROR: TLE was not loaded.\n===START OF DUMP")
            print(result)
            print("===END OF DUMP===")
            restore_port(port_path, modified_perms)
            return port_path

        arduino.reset_input_buffer()
        arduino.reset_output_buffer()
        print("Verifying...")
        arduino.write(b"\\@" + ARD_LINESEP)
        arduino.flush()
        arduino.reset_output_buffer()
        result = arduino.read(1000)
        if sat_name in result:
            print("TLE load successful.")
        else:
            print("TLE could not be located in the EEPROM file.\n===START OF DUMP")
            print(result)
            print("===END OF DUMP===")

    restore_port(port_path, modified_perms)


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
        help="Serial port connected to an Arduino; do not include `/dev/` from the path (typically ttyACM0)",
    )

    args = parser.parse_args()

    tle = retrieve_tle(args.norad_id)
    print(
        "TLE retrieved:"
        + (os.linesep * 2)
        + tle["tle0"]
        + os.linesep
        + tle["tle1"]
        + os.linesep
        + tle["tle2"]
        + os.linesep
    )

    program_tle(tle, args.port)


if __name__ == "__main__":
    main()
