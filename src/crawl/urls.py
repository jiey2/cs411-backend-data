from src.configs.configs import CRAWL_MIN_PRICE_ITEM, CRAWL_MAX_PRICE_ITEM

BUFF_ROOT = 'https://buff.163.com/'
BUFF_GOODS = BUFF_ROOT + 'api/market/goods?'
BUFF_HISTORY_PRICE = BUFF_ROOT + 'api/market/goods/price_history?'
BUFF_HISTORY_PRICE_CNY = BUFF_ROOT + 'api/market/goods/price_history/buff?'

def goods_section_root_url(category):
    base = BUFF_GOODS + 'game=csgo&page_num={}&sort_by=price.asc&min_price={}&max_price={}' \
        .format(900000 , CRAWL_MIN_PRICE_ITEM, CRAWL_MAX_PRICE_ITEM) #900000 is set to get actual page num
    if category is not None:
        base += '&category={}'.format(category)

    return base


def goods_section_page_url(category, page_num):
    base = BUFF_GOODS + 'game=csgo&page_num={}&sort_by=price.desc&min_price={}&max_price={}' \
        .format(page_num, CRAWL_MIN_PRICE_ITEM, CRAWL_MAX_PRICE_ITEM)
    if category is not None:
        base += '&category={}'.format(category)

    return base