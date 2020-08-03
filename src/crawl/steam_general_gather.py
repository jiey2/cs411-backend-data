import requests
from src.util.logger import log
import json

def get_raw_data():
    url = "http://api.steamanalyst.com/csgo/XHoXEDUxbtdHXFZlc"
    resp = requests.get(url)
    log.info("Fetching General Steam Community market data")
    if resp.ok == False:
        log.warning("Can't fetch Steam Community Market data ")
        return
    toReturn = resp.json()
    return toReturn['results']
