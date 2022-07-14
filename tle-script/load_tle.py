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
    print("\nTLE:\n" + tle + "\n")
    dev_filepath = "/dev/" + port
    try:
        dev_fd = os.open(dev_filepath, os.O_RDWR | os.O_NOCTTY | os.O_SYNC)
        old_attr = termios.tcgetattr(dev_fd)
        try:
            tty.setraw(dev_fd)

            active_attr = termios.tcgetattr(dev_fd)
            active_attr[4] = termios.B9600
            active_attr[5] = termios.B9600
            active_attr[6][termios.VMIN] = 12
            active_attr[6][termios.VTIME] = 5 # Wait until data is received, with 0.5-second inter-char wait
            termios.tcsetattr(dev_fd, termios.TCSAFLUSH, active_attr)

            tle_tx(dev_fd, tle, sat_name)
        finally:
            termios.tcsetattr(dev_fd, termios.TCSAFLUSH, old_attr) # Restore configuration
    finally:
        os.close(dev_fd)

    return

def tle_tx(dev_fd, tle, sat_name):
    # Flush any leftover commands
    os.write(dev_fd, "\n".encode('utf-8'))
    termios.tcflush(dev_fd, termios.TCIOFLUSH) 

    # Start TLE write
    os.write(dev_fd, "\#\n".encode('utf-8'))
    os.write(dev_fd, tle.encode('utf-8'))
    os.write(dev_fd, '\n\n'.encode('utf-8')) # End write
    termios.tcdrain(dev_fd)

    # Confirm TLE saved
    result = os.read(dev_fd, 1000)
    print("Result:\n"+ result.decode('utf-8') + "\n")
    if b"TLE corrupt" in result:
        print("ERROR: TLE was corrupted.\n===START OF TLE===")
        print(tle)
        print("===END OF TLE===")
        print(result)
        return
    if b"File was truncated" in result:
        print("ERROR: File was truncated due to lack of EEPROM storage.")
        return
    if sat_name.encode('utf-8') not in result:
        print("ERROR: TLE was not loaded.\n===START OF DUMP")
        print(result)
        print("===END OF DUMP===")
        return

    termios.tcflush(dev_fd, termios.TCIOFLUSH)
    os.write(dev_fd, "\@\n".encode('utf-8'))
    termios.tcdrain(dev_fd)
    result = os.read(dev_fd, 1000)
    print("Result2:\n"+ result.decode('utf-8') + "\n")
    if sat_name.encode('utf-8') in result:
        print("TLE load successful.")
        return
    else:
        print("TLE could not be located in the EEPROM file.\n===START OF DUMP")
        print(result)
        print("===END OF DUMP===")
        return



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Format: python3 load_tle.py [SatNOGS API JSON string] [serial port, like ttyACM0]")
    satnogs_str = sys.argv[1]
    ard_port = sys.argv[2]

    tle, sat_name = parse_json(satnogs_str)
    program_tle(tle, sat_name, ard_port)
