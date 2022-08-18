# FOR WRITE STATEMENT TESTING ONLY, WILL NOT CONNECT TO ARDUINO
$Params = @{
    format = "json"
    norad_cat_id = "41168"
}

$TLE_JSON = Invoke-WebRequest -Uri "https://db.satnogs.org/api/tle/" -Body $Params
poetry run python load_tle.py ($TLE_JSON -replace '"', '\"' ) trash