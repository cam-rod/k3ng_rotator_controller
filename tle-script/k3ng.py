import datetime
import logging
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
import serial
import timezone


@dataclass
class TLE:
    title: str
    line_one: str
    tine_two: str


@dataclass
class Satellite:
    id: int
    tle: TLE

    def __init__(self, sat_id):
        self.id = sat_id
        self.retrieve_tle()

    def retrieve_tle(self) -> TLE:
        params = {"format": "json", "norad_cat_id": str(self.id)}
        resp: requests.Response = requests.get(
            "https://db.satnogs.org/api/tle/", params=params
        ).json()

        # Some TLE titles start with "0 " (i.e. "0 ISS") and others don't ("ISS")
        # We opt to be consistent and NOT start with "0 ".
        if resp[0]["tle0"][0:1] == "0 ":
            self.tle.title = resp[0]["tle0"][2:]
        else:
            self.tle.title = resp[0]["tle0"]

        self.tle.line_one = resp[0]["tle1"]
        self.tle.line_two = resp[0]["tle2"]

        logging.info(f"Retrieved TLE for NORAD ID {self.id}: {self.tle}")

        return self.tle


class K3NG:
    def __init__(self, ser_port: str) -> None:
        # Ensure we have r/w
        self.port = Path(ser_port)
        if not self.port.exists():
            raise FileNotFoundError(self.port)

        if not os.access(
            self.port,
            os.R_OK | os.W_OK,
            effective_ids=(os.access in os.supports_effective_ids),
        ):
            # Attempt to chmod file
            if os.geteuid() != 0:
                logging.critical(
                    f"Unable to acquire read/write permissions on {self.port}.\n"
                    + "Please change permissions, or run this script as superuser."
                )
                sys.exit(1)

            logging.warning(f"Changing permissions on {self.port}")
            curr_mode: int = os.stat.S_IMODE(os.stat(self.port).st_mode)
            os.chmod(self.port, curr_mode | os.stat.S_IROTH | os.stat.S_IWOTH)

        self.ser = serial.Serial(ser_port, 9600, timeout=2, inter_byte_timeout=0.5)

        # This is just a dummy command to "prime" the connection
        # IDK why it's needed but the extended commands won't work otherwise
        self.query("\\-")

    #  ╭──────────────────────────────────────────────────────────╮
    #  │                     General Commands                     │
    #  ╰──────────────────────────────────────────────────────────╯

    def read(self) -> str:
        line = "0"
        response = []
        while line != b"":
            line = self.ser.readline()
            line_decoded = line.decode("utf-8")
            response.append(line_decoded.strip())
        logging.debug("RX: " + response)
        return response[:-1]

    def write(self, cmd: str) -> None:
        logging.debug("TX: cmd")
        self.ser.write((cmd + "\r").encode())
        self.ser.readline()
        self.ser.flush()

    def query(self, cmd) -> str:
        self.write(cmd)
        return self.read()

    def query_extended(self, cmd) -> str:
        if len(cmd) < 2 or "\\?" in cmd:
            raise ValueError("Invalid extended command")

        self.write("\\?" + cmd)

        try:
            resp = self.read()[0]
        except IndexError:
            raise RuntimeError("No response from rotator")

        status = resp[0:5]
        if "\\!??" in status:
            raise RuntimeError(f"Response error: {resp}")

        return resp[6:]

    def flush(self) -> str:
        self.write("\r")
        self.ser.flush()
        self.ser.reset_input_buffer()

    #  ╭──────────────────────────────────────────────────────────╮
    #  │                       Basic Config                       │
    #  ╰──────────────────────────────────────────────────────────╯

    def get_version(self) -> str:
        retval = self.query_extended("CV")
        return retval

    def get_time(self) -> str:
        retval = self.query("\\C")
        return retval

    def set_time(self, time: Optional[str] = None) -> None:
        if time is None:
            # Determine UTC time now
            current_time = datetime.now(tz=timezone.utc)
            time = current_time.strftime("%Y%m%d%H%M%S").encode("ascii")
            logging.debug(f"Setting to current UTC time: {current_time}")

        if len(time) != 14:
            raise ValueError("Invalid time length")

            self.query("\\O" + time)

    def get_loc(self) -> str:
        return self.query_extended("RG")[0]

    def set_loc(self, loc) -> None:
        if len(loc) != 6:
            raise ValueError("Invalid location length")

        self.query("\\G" + loc)

    def save_to_eeprom(self) -> None:
        self.query("\\Q")
        # This command restarts, so we reprime the buffer
        time.sleep(1)
        self.query("\\-")

    #  ╭──────────────────────────────────────────────────────────╮
    #  │                         Movement                         │
    #  ╰──────────────────────────────────────────────────────────╯

    def get_elevation(self) -> float:
        ret = self.query_extended("EL")
        return float(ret)

    def set_elevation(self, el: float) -> None:
        self.query_extended("GE" + ("%05.2f" % el))

    def get_azimuth(self) -> float:
        ret = self.query_extended("AZ")
        return float(ret)

    def set_azimuth(self, az: float) -> None:
        self.query_extended("GA" + ("%05.2f" % az))

    def rotate_down(self) -> None:
        self.query_extended("RD")

    def rotate_up(self) -> None:
        self.query_extended("RU")

    def rotate_left(self) -> None:
        self.query_extended("RL")

    def rotate_right(self) -> None:
        self.query_extended("RR")

    def stop_azimuth(self) -> None:
        self.query_extended("SA")

    def stop_elevation(self) -> None:
        self.query_extended("SE")

    def stop(self) -> None:
        self.query_extended("SS")

    #  ╭──────────────────────────────────────────────────────────╮
    #  │                       Calibration                        │
    #  ╰──────────────────────────────────────────────────────────╯

    def cal_full_up(self) -> None:
        self.query_extended("EF")

    def cal_full_down(self) -> None:
        self.query_extended("EO")

    def cal_full_cw(self) -> None:
        self.query_extended("AF")

    def cal_full_ccw(self) -> None:
        self.query_extended("AO")

    #  ╭──────────────────────────────────────────────────────────╮
    #  │                         Features                         │
    #  ╰──────────────────────────────────────────────────────────╯

    def get_autopark(self) -> str:
        ret = self.query("\\Y")
        return ret[0]

    def set_autopark(self, duration: int) -> str:
        # set to 0 for disable
        # duration in mins
        if duration == 0:
            return str(self.query("\\Y0"))
        else:
            return self.query("\\Y" + ("%04d" % duration))

    def load_tle(self, sat: Satellite) -> None:
        self.write("\\#")
        time.sleep(0.1)
        self.write(sat.tle.title)
        self.write(sat.tle.line_one)
        self.write(sat.tle.line_two)
        ret = self.query("\r")

        if "TLE corrupt" in ret:
            logging.critical("TLE corrupted on write")
            logging.info(ret)
            raise RuntimeError("TLE corrupted")
        if "File was truncated" in ret:
            logging.critical("File was truncated due to lack of EEPROM storage.")
            logging.info(ret)
            raise RuntimeError("TLE truncated")
        if sat.tle.title not in ret:
            logging.critical("TLE not loaded")
            logging.info(ret)
            raise RuntimeError("TLE not loaded")

    def read_tle(self) -> TLE:
        pass
