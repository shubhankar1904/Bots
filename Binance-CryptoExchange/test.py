import binance
import time
import binanceAPI
import datetime
'''
print "Order Book"
ob = binance.OrderBook().getOrderBook('TRXBTC',5)
print ob.get_last_update_id()
print ob.get_bids()
print ob.get_asks()
print ob.get_raw_data()
print "\n\n"
'''

'''
atl = binance.AggregateTradeList().getAggregateTrades("TRXBTC",limit=5)
print  atl[0].get_aggregate_trade_id()
print  atl[0].get_price()
print  atl[0].get_quantity()
print  atl[0].get_first_trade_id()
print  atl[0].get_last_trade_id()
print  atl[0].get_timestamp()
print  atl[0].get_buyer_maker_flag()
print  atl[0].get_best_price_trade()
'''

'''
cds = binance.CandleSticksList().getCandleSticks("TRXBTC",interval='1m', limit=5)
print cds[0].get_open_time()
print cds[0].get_open()
print cds[0].get_high()
print cds[0].get_low()
print cds[0].get_close()
print cds[0].get_volume()
print cds[0].get_close_time()
print cds[0].get_quote_asset_volume()
print cds[0].get_num_trades()
print cds[0].get_taker_buy_base_asset_volume()
print cds[0].get_taker_buy_quote_asset_volume()
'''

'''
spt = binance.SymbolPriceTicker()
spt.getPriceTickersData()
print spt.get_price_list()[0].get_price()
spt.getSymbolPriceTickerData("TRXBTC")
print spt.get_price_list().get_price()
'''


'''
odl = binance.OrderLists()
orders = odl.getOpenOrders("TRXBTC")
for order in orders:
    print str(order.get_order_id()) 
    print str(order.get_status())
    print order.get_side()
'''

'''
od = binance.Order(symbol = "TRXBTC", side = "SELL", type="LIMIT", quantity="500", price="0.00002000", timeInForce='GTC' ) 
print od.testOrder()
'''
    
#ud =  binanceAPI.UserDataAPI()
#print ud.testNewOrder(symbol='TRXBTC',side='BUY',type='STOP_LOSS_LIMIT',timeInForce='GTC' ,quantity='810',price='0.00000580', stopPrice='0.00000575')

'''
odl = binance.OrderLists()
orders = odl.getOpenOrders("TRXBTC")
for order in orders:
    print str(order.get_order_id()) 
    print str(order.get_status())
    print order.get_side()
    print order.get_orig_qty()
    print order.get_price()
    if(str(order.get_order_id()) == '19729010'):
        print order.cancelOrder()

    
    
'''
cdl = binance.CandleSticksList()

cdll=cdl.getCandleSticks(symbol="TRXBTC",interval='5m',limit='500',startTime="0",endTime=str(int((datetime.datetime(2017, 11, 01, 0, 0 ,00)- datetime.datetime(1970, 1, 1)).total_seconds() * 1000)))

for cdls in cdll:
     
   
    print datetime.datetime.fromtimestamp(cdls.get_open_time()/1000).strftime('%Y-%m-%d %H:%M:%S')
    print datetime.datetime.fromtimestamp(cdls.get_close_time()/1000).strftime('%Y-%m-%d %H:%M:%S')
    print cdls.get_open()
'''
def printFunc(msg):
    print msg
    
ws = binanceAPI.WebSocketsAPI()
ws.startTradeSocket("TRXBTC",printFunc)
ws.run()
'''