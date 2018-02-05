import datetime 
import time
import pymysql
import binance
import time
import binanceAPI
import datetime



from config import *       # This will allow us to use the keys as variables

import sys
from all_coin_pairs import *

connection = pymysql.connect()

cursor = connection.cursor() 


def getStartTime(coin):
    sql = "select MAX(close_time_stamp) from "+str(coin)
    cursor.execute(sql)
    max = cursor.fetchone()['MAX(close_time_stamp)']
    if max == None:
        return 0
    else:
        return max


for coin in coin_pairs:
               
    cursor.execute("CREATE TABLE if not exists "+coin+" (open_time DATETIME,open_time_stamp varchar(20), open decimal(15,10),\
     high decimal(15,10), low decimal(15,10), close decimal(15,10), volume decimal(25,10), close_time DATETIME,\
     close_time_stamp varchar(20), quote_asset_volume decimal(18,8), no_of_trades int, taker_buy_base_asset_volume decimal(20,10),\
     taker_buy_quote_asset_volume decimal(20,10));")
    connection.commit()
    
    sql = "INSERT INTO "+coin+" (open_time, open_time_stamp, open,high,low,\
    close,volume,close_time,close_time_stamp,quote_asset_volume,\
    no_of_trades,taker_buy_base_asset_volume,taker_buy_quote_asset_volume)\
     VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s);"
    
    cdl = binance.CandleSticksList()
    
    
    startTime="0"
    
    
    while(1):
       
        startTime = getStartTime(coin)
        cdll=cdl.getCandleSticks(symbol=coin,interval='5m',limit='5',startTime=startTime)
       
        if(len(cdll) == 0):
            break
        for cdls in cdll:
           
            cursor.execute(sql, (datetime.datetime.fromtimestamp(cdls.get_open_time()/1000).strftime('%Y-%m-%d %H:%M:%S'),\
                                cdls.get_open_time(),\
                                cdls.get_open(),\
                                cdls.get_high(),\
                                cdls.get_low(),\
                                cdls.get_close(),\
                                cdls.get_volume(),\
                                datetime.datetime.fromtimestamp(cdls.get_close_time()/1000).strftime('%Y-%m-%d %H:%M:%S'),\
                                cdls.get_close_time(),\
                                cdls.get_quote_asset_volume(),\
                                cdls.get_num_trades(),\
                                cdls.get_taker_buy_base_asset_volume(),\
                                cdls.get_taker_buy_quote_asset_volume()))
            startTime = cdls.get_close_time()
            print datetime.datetime.fromtimestamp(cdls.get_close_time()/1000).strftime('%Y-%m-%d %H:%M:%S')
        connection.commit()
    
