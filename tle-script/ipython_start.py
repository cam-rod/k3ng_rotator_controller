import logging
from argparse import ArgumentParser

from k3ng import K3NG, Satellite
from IPython import get_ipython


parser = ArgumentParser(
        prog="load_and_track.py",
        description="Loads a TLE and begins tracking it"
        )
parser.add_argument(
        "port",
        help="Serial port connected to an Arduino (typically /dev/ttyACM0)",
        )

logging.basicConfig(level=logging.INFO)

args = parser.parse_args()

rot = K3NG(args.port)

ipython = get_ipython()
ipython.run_line_magic("load_ext", "autoreload")
ipython.run_line_magic("autoreload", "2")
