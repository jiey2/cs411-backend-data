import pandas as pd
import json
import datetime

import numpy as np

from src.crawl.bitskins_gather import get_market_data as bit_gmd
from src.crawl.waxpeer_gather import get_market_data as waxp_gmd
from src.crawl.steam_general_gather import get_raw_data as stm_grd


def preprocess_buff_data(table):
    items = pd.DataFrame.from_dict(table)
    output = items[
        [
            "market_hash_name",
            "buy_max_price",
            "buy_num",
            "sell_min_price",
            "sell_num",
        ]
    ]
    curr_time = str(datetime.datetime.now().strftime("%Y-%m-%d--%H:%M"))
    output["update_time"] = curr_time

    return output


def preprocess_bitskins_data(table):
    items = pd.DataFrame(table)
    output = items[
        [
            "highest_price",
            "lowest_price",
            "market_hash_name",
            "recent_sales_info",
            "total_items",
            "updated_at",
        ]
    ]
    output['lowest_price'] = output['lowest_price'].str.replace(',', '')
    return output


def preprocess_waxpeer_data(table):
    items = pd.DataFrame(table)
    output = items[["name", "max", "avg", "count", "min",]]
    # Waxpeer pricing data: 1000 => $1
    output["max"] = output["max"] / 1000
    output["avg"] = output["avg"] / 1000
    output["min"] = output["min"] / 1000
    
    return output


def preprocess_steam_data(table):
    items = pd.DataFrame(table)

    return items


def snapshot_data():
    bit_tab = preprocess_bitskins_data(bit_gmd())
    bit_tab = bit_tab[["market_hash_name", "lowest_price", "total_items", "updated_at"]]
    waxp_tab = preprocess_waxpeer_data(waxp_gmd())
    waxp_tab = waxp_tab[["name", "min", "count"]]
    stm_tab = preprocess_steam_data(stm_grd())
    stm_tab = stm_tab[["market_name", "current_price", "sold_last_24h", "sold_last_7d"]]

    price_snapshot = stm_tab.set_index('market_name').join(bit_tab.set_index('market_hash_name'), how='outer')
    price_snapshot = price_snapshot.join(waxp_tab.set_index('name'), how='outer')

    # Final houskeeping get rid of NaN, change to None to use mySQL
    price_snapshot['current_price'] = price_snapshot['current_price'].str.replace(',', '')
    price_snapshot = price_snapshot.where(pd.notnull(price_snapshot), -1)
    return price_snapshot

def arbitrage_data():
    bit_tab = preprocess_bitskins_data(bit_gmd())
    bit_tab = bit_tab[["market_hash_name", "lowest_price", "total_items", "updated_at"]]
    waxp_tab = preprocess_waxpeer_data(waxp_gmd())
    waxp_tab = waxp_tab[["name", "min", "count"]]
    stm_tab = preprocess_steam_data(stm_grd())
    stm_tab = stm_tab[["market_name", "current_price", "sold_last_24h", "sold_last_7d"]]

    arb_tab = stm_tab.set_index('market_name').join(bit_tab.set_index('market_hash_name'), how='inner')
    arb_tab = arb_tab.join(waxp_tab.set_index('name'), how='inner')

    arb_tab = arb_tab.dropna(subset=['sold_last_24h'])

    # data cleaning string to float
    arb_tab['current_price'] = arb_tab['current_price'].str.replace(',', '')
    arb_tab = arb_tab.dropna()

    # Arbitrage requires a liquid market
    arb_tab = arb_tab[arb_tab.sold_last_24h.astype(float) > 0]

    arb_tab['absolute_margin'] = arb_tab[['current_price','lowest_price','min']].astype(float).max(axis=1) - arb_tab[['current_price','lowest_price','min']].astype(float).min(axis=1)
    arb_tab['percent_margin'] = arb_tab['absolute_margin'] / arb_tab[['current_price','lowest_price','min']].astype(float).min(axis=1)

    # Arbitrage requires relative high-value items
    # arb_tab = arb_tab[arb_tab.absolute_margin.astype(float) > 100]

    # Final housekeeping
    arb_tab = arb_tab.where((pd.notnull(arb_tab)), None)
    return arb_tab
