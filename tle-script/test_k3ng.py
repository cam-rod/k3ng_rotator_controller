from k3ng import K3NG

rotator = K3NG("/dev/ttyACM0")

print(rotator.get_version())
