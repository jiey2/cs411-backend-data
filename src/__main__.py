from src.crawl.bitskins_gather import get_market_data as get_bitskins
from src.crawl.crawl import crawl_buff
from src.data.datahandle import *
from src.mysql.sqlmaker import write_pricesnapshot_comb
from src.test import *

if __name__ == '__main__':
    """ Buff is unique handle all-in-one """
    buff_raw_data = crawl_buff() 

    data = snapshot_data()
    write_pricesnapshot_comb(data)


    