import json
import os
import sys
import termios
import tty

def parse_json(satnogs_str):
    tle_json = json.loads(satnogs_str)
    tle = tle_json[0]["tle0"] + '\n' \
        + tle_json[0]["tle1"] + '\n' \
        + tle_json[0]["tle2"]
    return tle, tle_json[0]["tle0"]

# Derived from https://blog.mbedded.ninja/programming/operating-systems/linux/linux-serial-ports-using-c-cpp/
def program_tle(tle, sat_name, port):
    dev_filepath = "/dev/" + port
    try:
        dev_fd = os.open(dev_filepath, os.O_RDWR | os.O_NOCTTY | os.O_SYNC)
        old_attr = termios.tcgetattr(dev_fd)
        try:
            tty.setraw(dev_fd)

            active_attr = termios.tcgetattr(dev_fd)
            active_attr[4] = termios.B9600
            active_attr[5] = termios.B9600
            active_attr[6][termios.VMIN] = 0
            active_attr[6][termios.VTIME] = 20 # Wait until data is received, with 2-second timeout
            termios.tcsetattr(dev_fd, termios.TCSAFLUSH, active_attr)

            tle_tx(dev_fd, tle, sat_name)
        finally:
            termios.tcsetattr(dev_fd, termios.TCSAFLUSH, old_attr) # Restore configuration
    finally:
        os.close(dev_fd)

    return

def tle_tx(dev_fd, sat_name, tle):
    # Flush any leftover commands
    os.write(dev_fd, "\n".encode('utf-8')) 
    os.read(dev_fd, 1000)

    # Start TLE write
    os.write(dev_fd, "\#\n".encode('utf-8'))
    os.read(dev_fd, 1000)
    os.write(dev_fd, tle.encode('utf-8'))
    os.write(dev_fd, '\n'.encode('utf-8')) # End write

    # Confirm TLE saved
    result = os.read(dev_fd, 1000)
    if result.find("TLE corrupt".encode('utf-8')):
        print("ERROR: TLE was corrupted.\n===START OF TLE===")
        print(tle)
        print("===END OF TLE===")
        return
    if result.find("File was truncated"):
        print("ERROR: File was truncated doe to lack of EEPROM storage.")
        return
    if result.find(sat_name) == -1:
        print("ERROR: TLE was not loaded.\n===START OF DUMP")
        print(result)
        print("===END OF DUMP===")
        return

    os.write("\@\n".encode('utf-8'))
    result = os.read(dev_fd, 1000)
    if result.find(sat_name):
        print("TLE load successful.")
        return



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Format: python3 load_tle.py [SatNOGS API JSON string] [serial port, like ttyACM0]")
    satnogs_str = sys.argv[1]
    ard_port = sys.argv[2]

    tle, sat_name = parse_json(satnogs_str)
    program_tle(tle, sat_name, ard_port)
