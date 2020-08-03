from src.crawl.bitskins_gather import get_market_data as bit_gmd
from src.data.datahandle import *
from src.crawl.waxpeer_gather import get_market_data as waxp_gmd
from src.crawl.steam_general_gather import get_raw_data as stm_grd
from src.mysql.sqlmaker import *

def testcase_bitskins():
    test_one = bit_gmd()
    toReturn = preprocess_bitskins_data(test_one)
    toReturn.to_csv('bit.csv')
    return toReturn

def testcase_waxpeer():
    test_ion = waxp_gmd()
    test_ion = preprocess_waxpeer_data(test_ion)
    test_ion.to_csv('waxp.csv')
    return test_ion

def test_innerjoin():
    bitp = testcase_bitskins()
    waxp = testcase_waxpeer()
    join = waxp.set_index('name').join(bitp.set_index('market_hash_name'), how = 'inner')
    join.to_csv('joined.csv')
    return join

def test_steam():
    stm = stm_grd()
    stm = preprocess_steam_data(stm)
    stm.to_csv('example_big.csv')
    return stm

def test_megatab():
    return snapshot_data()

def test_arbitrage_tab():
    return arbitrage_data()

def test_arb_tab_toSQL():
    write_arb_tab()
    return

def test_deleteSQL():
    mannul_delete_item("Sticker | Ork Waaagh!")
    return
    