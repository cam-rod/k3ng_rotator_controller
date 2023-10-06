from k3ng import K3NG

rotator = K3NG("/dev/ttyACM0")

print(rotator.get_version())
# rotator.rotate_up()
# sleep(2)
# rotator.stop()

print(rotator.get_autopark())
rotator.set_autopark(100)
print(rotator.get_autopark())
rotator.set_autopark(0)
print(rotator.get_autopark())

print(rotator.get_elevation())
print(rotator.get_azimuth())
