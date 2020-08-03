import re
import sys
import datetime

from forex_python.converter import CurrencyRates

from src.util.requester import get_json_dict
from src.crawl.urls import *
from src.util.logger import log
from src.mysql.sqlmaker import write_buff_data

## Request with right cookie

def collect_item(item):
    usdcnyrate = CurrencyRates().get_rate('USD', 'CNY')


    name = item['name']
    min_price = item['sell_min_price']
    sell_num = item['sell_num']

    try:
        min_price = float(min_price)
        min_price = min_price / usdcnyrate
    except:
        log.error("Cant' convert to USD")

    item_dictionary = {
        "ItemName": name,
        "BuffPrice": min_price,
        "BuffNum": sell_num,
        "BuffUpdateTime": int(datetime.datetime.now().timestamp())
    }

    return item_dictionary 

def crawl_buff(category=None):
    root_url = goods_section_root_url(category)
    log.info('GET: {}'.format(root_url))

    root_json = get_json_dict(root_url)

    if root_json is not None:
        if 'data' not in root_json:
            log.info('Error happens!')
            log.info(root_json)
            if 'error' in root_json:
                log.info('Error: ' + root_json['error'])
            sys.exit(1)

        total_page = root_json['data']['total_page']
        total_count = root_json['data']['total_count']
        log.info('Totally {} items of {} pages to crawl.'.format(total_count, total_page))
        # get each page

        # TEST CASE 
        for page_num in range(1, 3):
            log.info('Page {} / {}'.format(page_num, total_page))
            page_url = goods_section_page_url(category, page_num)
            page_json = get_json_dict(page_url)
            if page_json is not None:
                # items on this page
                items_json = page_json['data']['items']
                log.info("Process Data")
                for item in items_json:
                    items_dic = collect_item(item)
                    write_buff_data(items_dic)

    return




