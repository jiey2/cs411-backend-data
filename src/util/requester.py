import requests
import datetime
import random
import time

from requests import Timeout

from src.configs.configs import COOKIE, RETRY_TIMES
from src.util.logger import log

cookie_str = COOKIE
cookies = {}
for line in cookie_str.split(';'):
    k, v = line.split('=', 1)
    cookies[k] = v

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)  \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}

def sleep_awhile():
    interval = random.uniform(5, 6)
    log.info("sleep {}s at {}".format(interval, datetime.datetime.now()))
    time.sleep(interval)

def get_json_dict(url, times=1):
    if times > RETRY_TIMES:
        log.error('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, RETRY_TIMES))
        return None

    sleep_awhile()
    try:
        return requests.get(url, headers=headers, cookies=cookies, timeout=5).json()
    except Timeout:
        log.warn("timeout for {}. Try again.".format(url))
        return get_json_dict(url, times + 1)
