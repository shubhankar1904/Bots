from binanceAPI import MarketDataAPI,UserDataAPI
import decimal

md = MarketDataAPI()
ud = UserDataAPI()

class ServerTime(object):
    
    def getServerTime(self):
        data =  md.serverTime()
        try:
            return data['serverTime']
        except:
            return "Error Code:"+str(data['e'])+" -  "+data['msg']
            
class OrderBook(object):
    lastUpdateId = ''
    bids = [['price','qty']]
    asks = [['price','qty']]
    rawData = ''
    def extractBids(self,data):
        bidsData = data['bids']
        for bid in bidsData:
            self.bids += [[decimal.Decimal(bid[0]),decimal.Decimal(bid[1])]]
        
    def extractAsks(self,data):
        asksData = data['asks']
        for ask in asksData:
            self.asks += [[decimal.Decimal(ask[0]),decimal.Decimal(ask[1])]]
            
    def getOrderBook(self, symbol, limit = 100):
        data = md.orderBook(symbol, limit)
        self.lastUpdateId = data['lastUpdateId']
        self.extractBids(data)
        self.extractAsks(data)
        self.rawData = data
        return self

    def get_last_update_id(self):
        return self.lastUpdateId


    def get_bids(self):
        return self.bids


    def get_asks(self):
        return self.asks


    def get_raw_data(self):
        return self.rawData


    def set_last_update_id(self, value):
        self.lastUpdateId = value


    def set_bids(self, value):
        self.bids = value


    def set_asks(self, value):
        self.asks = value


    def set_raw_data(self, value):
        self.rawData = value

        
    
        
class AggregateTrade(object):
    aggregateTradeId = ''
    price = ''
    quantity = ''
    firstTradeId=''
    lastTradeId = ''
    timestamp = ''
    buyerMakerFlag = ''
    bestPriceTrade = ''
    
    def __init__(self, aggregateTradeId,price,quantity,firstTradeId,lastTradeId,timestamp,buyerMakerFlag, bestPriceTrade):
        
        self.aggregateTradeId = aggregateTradeId
        self.price = price
        self.quantity = quantity
        self.firstTradeId = firstTradeId
        self.lastTradeId = lastTradeId
        self.timestamp = timestamp
        self.buyerMakerFlag = buyerMakerFlag
        self.bestPriceTrade = bestPriceTrade
        
    

    def get_aggregate_trade_id(self):
        return self.aggregateTradeId


    def get_price(self):
        return self.price


    def get_quantity(self):
        return self.quantity


    def get_first_trade_id(self):
        return self.firstTradeId


    def get_last_trade_id(self):
        return self.lastTradeId


    def get_timestamp(self):
        return self.timestamp


    def get_buyer_maker_flag(self):
        return self.buyerMakerFlag


    def get_best_price_trade(self):
        return self.bestPriceTrade


    def set_aggregate_trade_id(self, value):
        self.aggregateTradeId = value


    def set_price(self, value):
        self.price = value


    def set_quantity(self, value):
        self.quantity = value


    def set_first_trade_id(self, value):
        self.firstTradeId = value


    def set_last_trade_id(self, value):
        self.lastTradeId = value


    def set_timestamp(self, value):
        self.timestamp = value


    def set_buyer_maker_flag(self, value):
        self.buyerMakerFlag = value


    def set_best_price_trade(self, value):
        self.bestPriceTrade = value

    
    
        
        
class AggregateTradeList(object):
    
    rawData = ''
    
    def createAggregateTradeList(self, data):
        agt_list = []
        for aggregateTrade in data:
            atObj = AggregateTrade(aggregateTradeId = aggregateTrade['a'],price = aggregateTrade['p'],quantity = aggregateTrade['q'],firstTradeId = aggregateTrade['f'], lastTradeId = aggregateTrade['l'], timestamp = aggregateTrade['T'], buyerMakerFlag = aggregateTrade['m'], bestPriceTrade = aggregateTrade['M'])
            agt_list.append(atObj)        
            
        self.rawData = data
        return agt_list
     
    def getAggregateTrades(self, symbol,fromId='',startTime='',endTime='',limit=''):
        data = md.aggregateTradesList(symbol,fromId,startTime,endTime,limit)
        self.rawData = data
        return self.createAggregateTradeList(data)
        
    
    def get_raw_data(self):
        return self.rawData


    def set_raw_data(self, value):
        self.rawData = value



class CandleSticks(object):
        openTime = ''
        open = ''
        high = ''
        low=''
        close = ''
        volume = ''
        closeTime = ''
        quoteAssetVolume = ''
        numTrades = ''
        takerBuyBaseAssetVolume = ''
        takerBuyQuoteAssetVolume = ''
        
        def __init__(self, openTime,open,high,low,close,volume,closeTime, quoteAssetVolume, numTrades, takerBuyBaseAssetVolume, takerBuyQuoteAssetVolume):
            
            self.openTime = openTime
            self.open = open
            self.high = high
            self.low = low
            self.close = close
            self.volume = volume
            self.closeTime = closeTime
            self.quoteAssetVolume = quoteAssetVolume
            self.numTrades = numTrades
            self.takerBuyBaseAssetVolume = takerBuyBaseAssetVolume
            self.takerBuyQuoteAssetVolume = takerBuyQuoteAssetVolume

        def get_open_time(self):
            return self.openTime


        def get_open(self):
            return self.open


        def get_low(self):
            return self.low


        def get_close(self):
            return self.close


        def get_volume(self):
            return self.volume


        def get_close_time(self):
            return self.closeTime


        def get_quote_asset_volume(self):
            return self.quoteAssetVolume


        def get_num_trades(self):
            return self.numTrades


        def get_taker_buy_base_asset_volume(self):
            return self.takerBuyBaseAssetVolume


        def get_taker_buy_quote_asset_volume(self):
            return self.takerBuyQuoteAssetVolume


        def get_high(self):
            return self.high


        def set_open_time(self, value):
            self.openTime = value


        def set_open(self, value):
            self.open = value

        def set_low(self, value):
            self.low = value


        def set_close(self, value):
            self.close = value


        def set_volume(self, value):
            self.volume = value


        def set_close_time(self, value):
            self.closeTime = value


        def set_quote_asset_volume(self, value):
            self.quoteAssetVolume = value


        def set_num_trades(self, value):
            self.numTrades = value


        def set_taker_buy_base_asset_volume(self, value):
            self.takerBuyBaseAssetVolume = value


        def set_taker_buy_quote_asset_volume(self, value):
            self.takerBuyQuoteAssetVolume = value


        def set_high(self, value):
            self.high = value

        
class CandleSticksList(object):
    rawData = ''
    
    def createCandleSticks(self, data):
        cds_list = []
        for candleStick in data:
            
            cds_list.append(\
            CandleSticks(openTime = candleStick[0],\
            open = candleStick[1],\
            high = candleStick[2],\
            low = candleStick[3],\
            close = candleStick[4],\
            volume = candleStick[5],\
            closeTime = candleStick[6],\
            quoteAssetVolume = candleStick[7],\
            numTrades = candleStick[8],\
            takerBuyBaseAssetVolume = candleStick[9],\
            takerBuyQuoteAssetVolume = candleStick[10]
            ))
        self.rawData = data
        return cds_list
            
    
    def getCandleSticks(self,symbol,interval, limit='', startTime='', endTime=''):
        data = md.candleSticks(symbol,interval, limit, startTime, endTime)
        self.rawData = data
        return self.createCandleSticks(data)
        
    
    def get_raw_data(self):
        return self.rawData


    def set_raw_data(self, value):
        self.rawData = value


class SymbolPrice(object):
    
    symbol =''
    price = ''
    
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price

    def get_symbol(self):
        return self.symbol


    def get_price(self):
        return self.price


    def set_symbol(self, value):
        self.symbol = value


    def set_price(self, value):
        self.price = value


class SymbolPriceTicker(object):
    rawData = ''
    priceList=[]
    
    def getPriceTickersData(self):
        data = md.symbolsPriceTicker()
        for symprices in data:
            self.priceList.append(SymbolPrice(symprices['symbol'],symprices['price']))
            
        self.rawData = data
        
        
        
    def getSymbolPriceTickerData(self, symbol):
        data = md.symbolPriceTicker(symbol)
        self.priceList=SymbolPrice(data['symbol'],data['price'])
        self.rawData = data    
        


    def get_raw_data(self):
        return self.rawData


    def get_price_list(self):
        return self.priceList


    def set_raw_data(self, value):
        self.rawData = value


    def set_price_list(self, value):
        self.priceList = value

        
        
        
        
class OrderBookTicker(object):
    
    Symbol = ''
    BidQty = ''
    BidPrice = ''
    AskQty = ''
    AskPrice = ''
    
    def __init__(self, symbol, bidQty, bidPrc, askQty, askPrc):
        self.Symbol = symbol
        self.BidQty = bidQty
        self.BidPrice = bidPrc
        self.AskQty = askQty
        self.AskPrice = askPrc

    def get_symbol(self):
        return self.Symbol


    def get_bid_qty(self):
        return self.BidQty


    def get_bid_price(self):
        return self.BidPrice


    def get_ask_qty(self):
        return self.AskQty


    def get_ask_price(self):
        return self.AskPrice


    def set_symbol(self, value):
        self.Symbol = value


    def set_bid_qty(self, value):
        self.BidQty = value


    def set_bid_price(self, value):
        self.BidPrice = value


    def set_ask_qty(self, value):
        self.AskQty = value


    def set_ask_price(self, value):
        self.AskPrice = value


class OrderBookTickerList(object):

  

    rawData = ''
    OBTList=[]
    
    def getOrderBookTickers(self):
        data = md.symbolsOrderBookTicker()
        for symprices in data:
            self.OBTList.append(OrderBookTicker(symprices['symbol'],symprices['bidQty'],symprices['bidPrice'],\
                             symprices['askQty'],symprices['askPrice']))
            
        self.rawData = data
        
        
        
    def getSymbolOrderBookTickers(self, symbol):
        data = md.symbolPriceTicker(symbol)
        for symprices in data:
            self.OBTList=OrderBookTicker(symprices['symbol'],symprices['bidQty'],symprices['bidPrice'],\
                             symprices['askQty'],symprices['askPrice'])
        self.rawData = data    

    
    def get_raw_data(self):
        return self.rawData


    def get_OBT_list(self):
        return self.OBTList


    def set_raw_data(self, value):
        self.rawData = value


    def set_OBT_list(self, value):
        self.OBTList = value
        



        
class Order(object):
    symbol=''    
    side = ''    
    type = ''    
    timeInForce =''    
    quantity = ''    
    price = ''    
    newClientOrderId = ''
    stopPrice = ''
    icebergQty = ''
    orderId=''
    origClientOrderId = ''
    recvWindow = ''
    orderStatus = ''
    clientOrderId = ''
    origQty = ''
    executedQty = ''
    status =''
    time = ''
    transactTime = ''
    
    rawdata = ''
    
    def __init__(self,symbol, side = '', type = '',\
    timeInForce ='', quantity = '', price = '', newClientOrderId = '',\
    stopPrice = '',icebergQty = '', orderId='', origClientOrderId = '',\
    recvWindow = '', orderStatus = '', clientOrderId = '', origQty = '',\
    executedQty = '', status ='', time = '', transactTime = ''):
        self.symbol = symbol.upper()
        self.side = side
        self.type = type
        self.timeInForce = timeInForce
        self.quantity = quantity
        self.price = price
        self.newClientOrderId = newClientOrderId
        self.stopPrice = stopPrice
        self.icebergQty = icebergQty
        self.orderId=orderId
        self.origClientOrderId = origClientOrderId
        self.recvWindow = recvWindow
        self.orderStatus = orderStatus
        self.clientOrderId = clientOrderId
        self.origQty = origQty
        self.executedQty = executedQty
        self.status =status
        self.time = time
        self.transactTime = transactTime
        
    
    def createOrder(self, symbol,side,type,quantity,price,timeInForce='',newClientOrderId='',stopPrice='',icebergQty=''):
        self.symbol = symbol
        self.side = side
        self.type = type
        self.timeInForce = timeInForce
        self.quantity = quantity
        self.price = price
        self.newClientOrderId = newClientOrderId
        self.stopPrice = stopPrice
        self.icebergQty = icebergQty
        
    def testOrder(self):
        return ud.testNewOrder(self.symbol,self.side,self.type,self.quantity,self.price,self.timeInForce,self.newClientOrderId,self.stopPrice,self.icebergQty)
    
    def sendOrder(self):
        data =  ud.testNewOrder(self.symbol,self.side,self.type,self.quantity,self.price,self.timeInForce,self.newClientOrderId,self.stopPrice,self.icebergQty)
        self.rawdata = data
        try:
           
            self.orderId = data['orderId']
            self.clientOrderId = data['clientOrderId']
            self.transactTime = data['transactTime']
            
        except:
            return data
    
    def orderStatus(self):
        data  = ud.orderStatus(self.symbol,self.orderId,self.origClientOrderId,self.recvWindow)
        
        self.symbol = data['symbol']
        self.orderId = data['orderId']
        self.clientOrderId = data['clientOrderId']
        self.price = data['price']
        self.origQty = data['origQty']
        self.executedQty = data['executedQty']
        self.status = data['status']
        self.timeInForce = data['timeInForce']
        self.type = data['type']
        self.side = data['side']
        self.stopPrice = data['stopPrice']
        self.icebergQty = data['icebergQty']
        self.time = data['time']
        
        return self.status
    
    def cancelOrder(self):
        data = ud.cancelOrder(self.orderId, self.origClientOrderId, self.newClientOrderId,self.recvWindow)
        self.rawdata = data
        try:
            self.origClientOrderId = data['origClientOrderId']
            self.orderId = data['orderId']
            self.clientOrderId = data['clientOrderId']
        except:
            return data

    def cancelOrder(self):
        return ud.cancelOrder(self.symbol,self.orderId,self.origClientOrderId, self.newClientOrderId,self.recvWindow)
    
    def get_symbol(self):
        return self.symbol


    def get_side(self):
        return self.side


    def get_type(self):
        return self.type


    def get_time_in_force(self):
        return self.timeInForce


    def get_quantity(self):
        return self.quantity


    def get_price(self):
        return self.price


    def get_new_client_order_id(self):
        return self.newClientOrderId


    def get_stop_price(self):
        return self.stopPrice


    def get_iceberg_qty(self):
        return self.icebergQty


    def get_order_id(self):
        return self.orderId


    def get_orig_client_order_id(self):
        return self.origClientOrderId


    def get_recv_window(self):
        return self.recvWindow


    def get_order_status(self):
        return self.orderStatus


    def get_client_order_id(self):
        return self.clientOrderId


    def get_orig_qty(self):
        return self.origQty


    def get_executed_qty(self):
        return self.executedQty


    def get_status(self):
        return self.status


    def get_time(self):
        return self.time


    def get_transact_time(self):
        return self.transactTime


    def get_rawdata(self):
        return self.rawdata


    def set_symbol(self, value):
        self.symbol = value


    def set_side(self, value):
        self.side = value


    def set_type(self, value):
        self.type = value


    def set_time_in_force(self, value):
        self.timeInForce = value


    def set_quantity(self, value):
        self.quantity = value


    def set_price(self, value):
        self.price = value


    def set_new_client_order_id(self, value):
        self.newClientOrderId = value


    def set_stop_price(self, value):
        self.stopPrice = value


    def set_iceberg_qty(self, value):
        self.icebergQty = value


    def set_order_id(self, value):
        self.orderId = value


    def set_orig_client_order_id(self, value):
        self.origClientOrderId = value


    def set_recv_window(self, value):
        self.recvWindow = value


    def set_order_status(self, value):
        self.orderStatus = value


    def set_client_order_id(self, value):
        self.clientOrderId = value


    def set_orig_qty(self, value):
        self.origQty = value


    def set_executed_qty(self, value):
        self.executedQty = value


    def set_status(self, value):
        self.status = value


    def set_time(self, value):
        self.time = value


    def set_transact_time(self, value):
        self.transactTime = value


    def set_rawdata(self, value):
        self.rawdata = value

    
class OrderLists(object):
    odList = []
    
    def getOpenOrders(self,symbol,recvWindow=''):
        data = ud.openOrders(symbol,recvWindow)
        self.odList=[]
        for order in data:
            
            self.odList.append(Order(symbol = order['symbol'], orderId=order['orderId'],\
                                clientOrderId = order['clientOrderId'], price = order['price'], origQty = order['origQty'],\
                                executedQty = order['executedQty'], status=order['status'], timeInForce=order['timeInForce'],\
                                type = order['type'], side=order['side'], stopPrice = order['stopPrice'], icebergQty = order['icebergQty'],\
                                time =  order['time']
                                ))
            
        return self.odList
        
        
    def getAllOrders(object):
        data = ud.allOrders(symbol,recvWindow='')
        self.odList=[]
        for order in data:
            
            self.odList.append(Order(symbol = order['symbol'], orderId=order['orderId'],\
                                clientOrderId = order['clientOrderId'], price = order['price'], origQty = order['origQty'],\
                                executedQty = order['executedQty'], status=order['status'], timeInForce=order['timeInForce'],\
                                type = order['type'], side=order['side'], stopPrice = order['stopPrice'], icebergQty = order['icebergQty'],\
                                time =  order['time']
                                ))
            
        return self.odList