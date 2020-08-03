import pyotp
import requests
import sys
import json

from src.configs.credentials import BITSKINS_API_KEY, BITSKINS_TWO_FACTOR_SECRET
from src.util.logger import log

## Credentials
my_secret = BITSKINS_TWO_FACTOR_SECRET
my_token = pyotp.TOTP(my_secret)
API_KEY = BITSKINS_API_KEY
CODE = my_token.now()

APP_ID = '730'

def get_market_data():
    url = 'https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key=' + API_KEY + '&code=' + CODE + '&app_id=' + APP_ID
    resp = requests.get(url)
    log.info("Fetching Bitskins market data")
    if resp.ok == False:
        log.warning("Can't fetch Bitskins data ")
        return
    price_list = resp.json()
    return price_list['data']['items']




