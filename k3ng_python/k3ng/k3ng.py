import datetime
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
import serial

SEND_DELAY = 0.03
RECV_DELAY = 0.03


@dataclass
class TLE:
    title: str
    line_one: str
    line_two: str


@dataclass
class Satellite:
    id: int
    tle: TLE

    def __init__(self, sat_id: int, tle: Optional[TLE] = None):
        self.id = sat_id
        if tle is None:
            self.retrieve_tle()
        else:
            self.tle = tle

    def retrieve_tle(self) -> TLE:
        params = {"format": "json", "norad_cat_id": str(self.id)}
        resp = requests.get("https://db.satnogs.org/api/tle/", params=params).json()

        # Some TLE titles start with "0 " (i.e. "0 ISS") and others don't ("ISS")
        # We opt to be consistent and NOT start with "0 ".
        if resp[0]["tle0"][0:2] == "0 ":
            self.tle = TLE(resp[0]["tle0"][2:], resp[0]["tle1"], resp[0]["tle2"])
        else:
            self.tle = TLE(resp[0]["tle0"], resp[0]["tle1"], resp[0]["tle2"])

        # K3NG doesn't like special characters or spaces
        self.tle.title = re.sub("[^A-Za-z0-9 ]+", "", self.tle.title)
        self.tle.title = self.tle.title.replace(" ", "")

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
            if os.geteuid() != 0:
                logging.critical(
                    f"Unable to acquire read/write permissions on {self.port}.\n"
                    + "Please change permissions, or run this script as superuser."
                )
                sys.exit(1)

        self.ser = serial.Serial(ser_port, 9600, timeout=1, inter_byte_timeout=0.5)
        self.flush()

        # This is just a dummy command to "prime" the connection
        # IDK why it's needed but the extended commands won't work otherwise
        ret = self.query("\\-")
        if ret == []:
            raise RuntimeError("Unable to communicate with rotator")

    #  ╭──────────────────────────────────────────────────────────╮
    #  │                     General Commands                     │
    #  ╰──────────────────────────────────────────────────────────╯

    def read(self) -> list[str]:
        response = []
        line = ""

        while self.ser.in_waiting > 0:
            time.sleep(RECV_DELAY)
            ch = self.ser.read()
            ch_decoded = ch.decode("utf-8")
            if ch_decoded == "\r" or ch_decoded == "\n":
                response.append(line)
                line = ""
            else:
                line += ch_decoded

        response = list(filter(None, response))

        logging.debug("RX: " + str(response))
        return response

    def write(self, cmd: str) -> None:
        logging.debug(f"TX: {cmd}")
        for i in cmd[0]:
            time.sleep(SEND_DELAY)
            self.ser.write(cmd.encode())
        time.sleep(SEND_DELAY)
        self.ser.write(("\r").encode())
        time.sleep(0.2)
        self.ser.readline()

    def query(self, cmd) -> list[str]:
        self.write(cmd)
        time.sleep(0.2)
        return self.read()

    def query_extended(self, cmd) -> str:
        time.sleep(0.2)
        if len(cmd) < 2 or "\\?" in cmd:
            raise ValueError("Invalid extended command")

        self.write("\\?" + cmd)

        time.sleep(0.2)

        try:
            resp = self.read()[0]
        except IndexError:
            raise RuntimeError("No response from rotator")

        status = resp[0:5]
        if "\\!??" in status:
            raise RuntimeError(f"Response error: {resp}")

        if "OK" not in status:
            raise RuntimeError(f"Invalid response: {resp}")

        return resp[6:]

    def flush(self) -> None:
        self.write("\r")
        self.ser.flush()
        self.ser.reset_input_buffer()

    #  ╭──────────────────────────────────────────────────────────╮
    #  │                       Basic Config                       │
    #  ╰──────────────────────────────────────────────────────────╯

    def get_version(self) -> str:
        retval = self.query_extended("CV")
        return retval

    def get_time(self) -> datetime.datetime:
        retval = self.query("\\C")
        return datetime.datetime.fromisoformat(retval[0])

    def set_time(self, time: Optional[str] = None) -> None:
        if time is None:
            # Determine UTC time now
            current_time = datetime.datetime.now(tz=datetime.timezone.utc)
            time = current_time.strftime("%Y%m%d%H%M%S")
            logging.debug(f"Setting to current UTC time: {current_time}")

        if len(time) != 14:
            raise ValueError("Invalid time length")

        ret = self.query("\\O" + time)
        ret_split = " ".join(ret[0].split(" ")[3:5])
        ret_time = datetime.datetime.fromisoformat(ret_split)

        if abs(ret_time - current_time) > datetime.timedelta(seconds=10):
            raise ValueError("Time did not save!")

        self.check_time()

    def check_time(self):
        current_time = datetime.datetime.now(tz=datetime.timezone.utc)
        ret_time = self.get_time()

        if abs(ret_time - current_time) > datetime.timedelta(seconds=10):
            logging.warning("Time difference greater than 10 seconds!")

    def get_loc(self) -> str:
        # TODO: make this be able to return coords or grid
        return self.query_extended("RG")[0]

    def set_loc(self, loc) -> None:
        if len(loc) != 6:
            raise ValueError("Invalid location length")

        self.query("\\G" + loc)

        # TODO: check retval

    def save_to_eeprom(self) -> None:
        self.write("\\Q")
        # This command restarts, so we reprime the buffer
        time.sleep(1)
        self.flush()
        self.query("\\-")

    #  ╭──────────────────────────────────────────────────────────╮
    #  │                         Movement                         │
    #  ╰──────────────────────────────────────────────────────────╯

    def get_elevation(self) -> float:
        ret = self.query_extended("EL")
        # replace is to accomodate for a quirk in reporting at EL=0
        return float(ret.replace("0-0.", "00.").strip("0"))

    def set_elevation(self, el: float) -> None:
        self.query_extended("GE" + ("%05.2f" % el))

    def get_azimuth(self) -> float:
        ret = self.query_extended("AZ")
        return float(ret.strip("0"))

    def set_azimuth(self, az: float) -> None:
        self.query_extended("GA" + ("%05.2f" % az))

    def down(self) -> None:
        self.query_extended("RD")

    def up(self) -> None:
        self.query_extended("RU")

    def left(self) -> None:
        self.query_extended("RL")

    ccw = left

    def right(self) -> None:
        self.query_extended("RR")

    cw = right

    def stop_azimuth(self) -> None:
        self.query_extended("SA")

    def stop_elevation(self) -> None:
        self.query_extended("SE")

    def stop(self) -> None:
        self.query_extended("SS")

    #  ╭──────────────────────────────────────────────────────────╮
    #  │                       Calibration                        │
    #  ╰──────────────────────────────────────────────────────────╯

    def cal_full_up(self) -> int:
        ret = self.query_extended("EF")
        return int(ret)

    def cal_full_down(self) -> int:
        ret = self.query_extended("EO")
        return int(ret)

    def cal_full_cw(self) -> int:
        ret = self.query_extended("AF")
        return int(ret)

    def cal_full_ccw(self) -> int:
        ret = self.query_extended("AO")
        return int(ret)

    #  ╭──────────────────────────────────────────────────────────╮
    #  │                         Features                         │
    #  ╰──────────────────────────────────────────────────────────╯

    def park(self) -> None:
        ret = self.query("\\P")
        if "Parking" not in ret[0]:
            raise RuntimeError("Not parking")

    def get_autopark(self) -> int:
        ret = self.query("\\Y")
        if "Autopark is off" in ret[0]:
            return 0
        else:
            return int(ret[0].split()[4])

    # WARNING: autopark updates itself every few seconds.
    # ADC drift may cause the rotator to slightly adjust itself between updates,
    #   meaning this parked in location (mostly), but not in lack of motion.
    def set_autopark(self, duration: int) -> None:
        # set to 0 for disable
        # duration in mins
        if duration == 0:
            ret = self.query("\\Y0")
            if "off" not in ret[0]:
                raise RuntimeError(f"Autopark not set ({ret[0]})")
        else:
            ret = self.query("\\Y" + ("%04d" % duration))
            if f"{duration} minute" not in ret[0]:
                raise RuntimeError(f"Autopark not set ({ret[0]})")

    def set_park_location(self, az: int, el: int) -> None:
        ret = self.query(f"\\PA{az:03}")
        if str(az) not in ret[0]:
            raise RuntimeError("Azimuth park not set")

        ret = self.query(f"\\PE{el:03}")
        if str(el) not in ret[0]:
            raise RuntimeError("Elevation park not set")

    def get_park_location(self) -> tuple[int, int]:
        ret = self.query("\\PA")
        ret_split = ret[0].split(" ")
        return (int(ret_split[2]), int(ret_split[4]))

    def load_tle(self, sat: Satellite) -> None:
        self.write("\\#")
        time.sleep(0.5)
        self.write(sat.tle.title)
        self.write(sat.tle.line_one)
        self.write(sat.tle.line_two)
        self.write("\r")
        time.sleep(0.5)
        ret = self.read()

        if "corrupt" in ret[0]:
            logging.critical("TLE corrupted on write")
            logging.info(ret)
            raise RuntimeError("TLE corrupted")
        if "truncated" in ret[0]:
            logging.critical("File was truncated due to lack of EEPROM storage.")
            logging.info(ret)
            raise RuntimeError("TLE truncated")
        if sat.tle.title not in ret[1]:
            logging.critical("TLE not loaded")
            logging.info(ret)
            raise RuntimeError("TLE not loaded")

    def read_tles(self) -> list[TLE]:
        ret = self.query("\\@")

        tles = []

        i = 1
        while ret[i] != "":
            tles.append(TLE(ret[i], ret[i + 1], ret[i + 2]))
            i = i + 3

        return tles

    def clear_tles(self) -> None:
        ret = self.query("\\!")
        if "Erased the TLE file area" not in ret[0]:
            raise RuntimeError("Failed to clear TLEs")

    def get_trackable(self) -> list[str]:
        ret = self.query("\\|")
        return ret

    def get_tracking_status(self) -> list[str]:
        ret = self.query("\\~")
        return ret

    def select_satellite(self, sat: Satellite) -> None:
        ret = self.query("\\$" + sat.tle.title[0:5])

        if "Loading" not in ret[1]:
            raise RuntimeError("Unable to select satellite")

    def get_next_pass(self, satellite) -> list[str]:
        return self.query(f"\\%{satellite.name[0:6]}")

    def enable_tracking(self) -> None:
        self.query("\\^1")
        # you get the idea

    def disable_tracking(self) -> None:
        self.query("\\^0")
        # samesies

    def load_and_track(self, sat_id: int) -> None:
        """Helper to load and begin tracking a satellite"""
        sat = Satellite(sat_id)
        self.set_time()
        self.load_tle(sat)
        self.check_time()
        self.select_satellite(sat)
        self.enable_tracking()
        self.get_tracking_status()
