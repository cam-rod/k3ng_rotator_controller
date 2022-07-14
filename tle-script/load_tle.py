import json
from time import sleep
import sys
import serial # Converts

def parse_json(satnogs_str):
    tle_json = json.loads(satnogs_str)
    tle = tle_json[0]["tle0"] + '\r' \
        + tle_json[0]["tle1"] + '\r' \
        + tle_json[0]["tle2"]

    print("\nTLE:\n" + tle.replace("\r", "\r\n") + "\n")
    return tle, tle_json[0]["tle0"]

# Derived from https://blog.mbedded.ninja/programming/operating-systems/linux/linux-serial-ports-using-c-cpp/
def program_tle(tle, sat_name, port):
    dev_filepath = "/dev/" + port

    with serial.Serial(dev_filepath, 9600, timeout=2, inter_byte_timeout=0.5) as arduino:
        print("Flushing leftover data...")
        arduino.write("\r".encode('utf-8'))
        arduino.flush()
        arduino.reset_input_buffer()

        print("Writing TLE...")
        arduino.write("\#\r".encode('utf-8'))
        arduino.write(tle.encode('utf-8'))
        arduino.write("\r\r".encode('utf-8'))
        arduino.flush()
        arduino.reset_input_buffer()

        # Confirm TLE saved
        result = arduino.read(1000)
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

        arduino.reset_input_buffer()
        arduino.reset_output_buffer()
        print("Verifying...")
        arduino.write("\@\r".encode('utf-8'))
        arduino.flush()
        arduino.reset_input_buffer()
        result = arduino.read(1000)
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
