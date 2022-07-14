import serial

with serial.Serial("/dev/ttyACM0", timeout=5) as ard:
    print(ard.name)
    ard.write("\C\r\n".encode('utf-8'))
    print(ard.read(size=20))