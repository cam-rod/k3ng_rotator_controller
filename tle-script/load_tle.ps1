$TLE_JSON = curl "https://db.satnogs.org/api/tle/?format=json&norad_cat_id=$args[0]"
python load_tle.py "$TLE_JSON" trash