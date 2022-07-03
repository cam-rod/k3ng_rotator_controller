#!/bin/bash

# Format: load_tle.sh [NORAD_cat_id, like 41168] [port, like ttyACM0]
sudo chmod a+rw /dev/$2
tle_json=$(curl "https://db.satnogs.org/api/tle/?format=json&norad_cat_id=$1")
python3 load_tle.py "$tle_json" $2
unset tle_json
sudo chmod o-rw /dev/$2
