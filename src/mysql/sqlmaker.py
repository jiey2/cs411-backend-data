import mysql.connector
import datetime

from src.configs.credentials import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE
from src.data.datahandle import arbitrage_data
from src.util.logger import log

def open_db():
    mydb = mysql.connector.connect(
    host = DB_HOST,
    user = DB_USER,
    passwd = DB_PASSWORD,
    database = DB_DATABASE
    )
    return mydb

def write_buff_data(item_dic):
    log.info("Writing to SQL: " + str(item_dic))
    ItemName = item_dic['ItemName']
    BuffPrice = item_dic['BuffPrice']
    BuffNum = item_dic['BuffNum']
    BuffUpdateTime = item_dic['BuffUpdateTime']

    mydb = open_db()
    myDBcursor = mydb.cursor()

    table = "PriceSnapshot"

    sql = "USE CSGO"
    myDBcursor.execute(sql)
    sql = f"""INSERT INTO {table} (ItemName, BuffPrice, BuffNum, BuffUpdateTime) VALUES ("{ItemName}",{BuffPrice},{BuffNum},{BuffUpdateTime}) ON DUPLICATE KEY UPDATE \
        BuffPrice={BuffPrice}, BuffNum={BuffNum}, BuffUpdateTime={BuffUpdateTime}"""
    myDBcursor.execute(sql)

    mydb.commit()
    myDBcursor.close()
    mydb.close()

    return

def write_pricesnapshot_comb(input_df):
    input_df = input_df.reset_index()
    item_list = input_df.values.tolist()

    mydb = open_db()
    myDBcursor = mydb.cursor()
    sql = "USE CSGO"
    myDBcursor.execute(sql)
    table = "PriceSnapshot"

    for row in item_list:
        log.info("Combined data writing to SQL: " + str(row[0]))
        ItemName = row[0]
        SteamPrice = float(row[1])
        SteamDayVolume = int(row[2])
        SteamWeekVolume = int(row[3])
        SteamUpdateTime = int(datetime.datetime.now().timestamp())
        BitskinsPrice = float(row[4])
        BitskinsNum = int(row[5])
        BitSkinsUpdateTime = int(row[6])
        WaxpeerPrice = float(row[7])
        WaxpeerNum = int(row[8])
        WaxpeerUpdateTime = int(datetime.datetime.now().timestamp())

        sql = f"""INSERT INTO {table} (ItemName, SteamPrice, SteamDayVolume, SteamWeekVolume, SteamUpdateTime, BitskinsPrice, BitskinsNum, BitSkinsUpdateTime, \
            WaxpeerPrice, WaxpeerNum, WaxpeerUpdateTime ) \
                VALUES ("{ItemName}",{SteamPrice},{SteamDayVolume},{SteamWeekVolume},{SteamUpdateTime},{BitskinsPrice},{BitskinsNum},{BitSkinsUpdateTime},\
                {WaxpeerPrice},{WaxpeerNum},{WaxpeerUpdateTime}) \
                    ON DUPLICATE KEY UPDATE \
                        SteamPrice={SteamPrice}, SteamDayVolume={SteamDayVolume}, SteamWeekVolume={SteamWeekVolume}, SteamUpdateTime={SteamUpdateTime}, BitskinsPrice={BitskinsPrice}, BitskinsNum={BitskinsNum}\
                            , BitSkinsUpdateTime={BitSkinsUpdateTime}, WaxpeerPrice={WaxpeerPrice}, WaxpeerNum={WaxpeerNum}, WaxpeerUpdateTime={WaxpeerUpdateTime}
        """
        myDBcursor.execute(sql)
    mydb.commit()
    myDBcursor.close()
    mydb.close()
    


    return        






def form_price_snapshot():
    return


def write_arb_tab():
    curr_arb_tab = arbitrage_data()
    curr_arb_tab = curr_arb_tab.reset_index()
    print(curr_arb_tab)

    mydb = open_db()
    myDBcursor = mydb.cursor()
    table = 'ArbTable'

    myDBcursor.execute("DROP TABLE IF EXISTS " + table)

    sql_create_tab = "CREATE TABLE " + table + " \
         (ItemName VARCHAR(50), SteamPrice DECIMAL(10,2), SteamDayVolume INTEGER, \
             SteamWeekVolume INTEGER, BitskinsPrice DECIMAL(10,2), BitskinsNum INTEGER, \
                 UpdateTime INTEGER, WaxpeerPrice DECIMAL(10,2), WaxpeerNum INTEGER, \
                     AbsoluteProfit DECIMAL(10,5), PercentProfit DECIMAL(10,5) )"
    myDBcursor.execute(sql_create_tab)

    cols = "ItemName, SteamPrice, SteamDayVolume, SteamWeekVolume, BitskinsPrice, BitskinsNum, \
        UpdateTime, WaxpeerPrice, WaxpeerNum, AbsoluteProfit, PercentProfit"
    for i,row in curr_arb_tab.iterrows():
        log.info('Writing Arbitrage Table into SQL ' + str(tuple(row)))
        sql = "INSERT INTO " + table + " (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        myDBcursor.execute(sql, tuple(row))
    
    mydb.commit()
    myDBcursor.close()
    mydb.close()
    return

def mannul_delete_item(itemToDelete):
    mydb = open_db()
    myDBcursor = mydb.cursor()
    table = 'ArbTable'

    sql_delete = " DELETE FROM " + table + " WHERE " + "ItemName = '" + itemToDelete + "'"
    log.info(sql_delete)
    myDBcursor.execute(sql_delete)
    mydb.commit()
    myDBcursor.close()
    mydb.close()
    return




