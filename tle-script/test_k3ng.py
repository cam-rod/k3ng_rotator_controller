import logging
from time import sleep

from k3ng import K3NG

logging.basicConfig(level=logging.DEBUG)
rotator = K3NG("/dev/ttyACM0")

print(rotator.get_version())
print(rotator.get_time())

print(rotator.read_tles())
print(rotator.get_tracking_status())

# print(rotator.get_autopark())
# rotator.set_autopark(100)
# print(rotator.get_autopark())
# rotator.set_autopark(0)
# print(rotator.get_autopark())

print(rotator.get_elevation())
print(rotator.get_azimuth())
