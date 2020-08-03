import requests
import json

from src.util.logger import log

def get_market_data():
    url = 'https://api.waxpeer.com/v1/prices?game=csgo&min_price=0&max_price=100000000'
    resp = requests.get(url)
    log.info("Fetching Waxpeer market data")
    if resp.ok == False:
        log.warning("Can't fetch Waxpeer data ")
        return
    price_list = resp.json()
    return price_list['items']
