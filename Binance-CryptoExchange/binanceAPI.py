import config
import utils
import json
import time
import datetime
import pandas
import ast
from json2table import convert
from websocket import create_connection
#import websocket
import logging
import protocols
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
from twisted.internet import ssl
import requests
import threading

class BinanceAPI(object):
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    POST = "POST"
    
        
    def hitBinanceWebAPI(self, method, url,param='',signed=False):
        url="https://api.binance.com"+url
        headers={'X-MBX-APIKEY':config.getApiKey()}
        
        if(not signed):
            
            
            try:
                r = requests.request(method = method.upper(), url = url, params = param, headers=headers)        
                data = r.json()
                return data
            except requests.exceptions.ConnectionError as e:
                err = {'e':100, 'msg':'Unable to connect to network'}
                data = json.loads(json.dumps(err))
            except  e:
                err = {'e':100, 'msg':str(e)}
                data = json.loads(json.dumps(err))
            return data    
                
        else:
            
            if(param!=''):
                msg = utils.getQueryString(param)
            
            signature = utils.getSignature(msg)
            
            param.update({"signature":signature})
            print param
            try:
                r = requests.request(method=method.upper(), url=url, headers=headers, params=param)
                data=r.json()
            except requests.exceptions.ConnectionError as e:
                err = {'e':100, 'msg':'Unable to connect to network'}
                data = json.loads(json.dumps(err))
            except  e:
                err = {'e':100, 'msg':str(e)}
                data = json.loads(json.dumps(err))
            
            return data
        
    def checkConnection(self):
        URL="/api/v1/ping"
        data = self.hitBinanceWebAPI(method='GET' , url=URL)
        try:
            if(len(data) != 0):
                print("Unable to connect to Binance")
                return 0
        except:
            print("Unable to connect to Binance")
            return 0
        
        return 1

    
class MarketDataAPI(BinanceAPI):

    
    def __init__(self):
        return
        
    def serverTime(self):
        url="/api/v1/time"    
        data=self.hitBinanceWebAPI(method=self.GET, url=url)
        return data

    def orderBook(self,symbol,limit=100):
        url="/api/v1/depth"
        params = {'symbol':symbol,'limit':limit}
        
        data=self.hitBinanceWebAPI(method=self.GET, url=url, param=params)
        return data

    def aggregateTradesList(self,symbol,fromId='',startTime='',endTime='',limit=''):
        '''
        Name        Type    Mandatory    Description
        symbol        STRING    YES    
        fromId        LONG    NO    ID to get aggregate trades from INCLUSIVE.
        startaTime    LONG    NO    Timestamp in ms to get aggregate trades from INCLUSIVE.
        endTime        LONG    NO    Timestamp in ms to get aggregate trades until INCLUSIVE.
        limit         INT        NO    Default 500; max 500.
        '''
        url="/api/v1/aggTrades"
        params={'symbol':symbol}
        if(fromId!=''):
            params.update({'fromId':fromId})
        if(startTime!=''):
            params.update({'startTime':startTime})
        if(endTime!=''):
            params.update({'endTime':endTime})
        if(limit!=''):
            params.update({'limit':limit})
        
        data=self.hitBinanceWebAPI(self.GET, url,params)
        return data
            
    def candleSticks(self,symbol,interval, limit='', startTime='', endTime=''):
        '''
        Name        Type    Mandatory    Description
        symbol        STRING    YES    
        interval    ENUM    YES    
        limit        INT        NO        Default 500; max 500.
        startTime    LONG    NO    
        endTime        LONG    NO    
        '''
        url="/api/v1/klines"
        params={'symbol':symbol,'interval':interval}
        
        if(startTime!=''):
            params.update({'startTime':startTime})
        if(endTime!=''):
            params.update({'endTime':endTime})
        if(limit!=''):
            params.update({'limit':limit})
        
        data=self.hitBinanceWebAPI(self.GET, url,params)
        return data
            
    def symbolsPriceTicker(self):
        url='/api/v1/ticker/allPrices'
        data=self.hitBinanceWebAPI(self.GET, url)
        return data

    def symbolPriceTicker(self,symbol):
        url='/api/v1/ticker/allPrices'
        data=self.hitBinanceWebAPI(self.GET, url)
        
        for price in data:
            if(price['symbol']==symbol):
                return price
        
        return -1
                        
    def symbolsOrderBookTicker(self):
        url='/api/v1/ticker/allBookTickers'
        data=self.hitBinanceWebAPI(self.GET, url)
        return data
        
    def symbolOrderBookTicker(self,symbol):
        url='/api/v1/ticker/allBookTickers'
        data=self.hitBinanceWebAPI(self.GET, url)
        for price in data:
            if(price['symbol']==symbol):
                return price
        
        return -1


class UserDataAPI(BinanceAPI):

    def __init__(self):
        return

    def newOrder(self,symbol,side,type,quantity,price,timeInForce='',newClientOrderId='',stopPrice='',icebergQty=''):
        '''
        Name                Type    Mandatory    Description
        symbol                STRING    YES    
        side                ENUM    YES    
        type                ENUM    YES    
        timeInForce            ENUM    YES    
        quantity            DECIMAL    YES    
        price                DECIMAL    YES    
        newClientOrderId    STRING    NO    A unique id for the order. Automatically generated if not sent.
        stopPrice            DECIMAL    NO    Used with stop orders
        icebergQty            DECIMAL    NO    Used with iceberg orders
        timestamp            LONG    YES    
        '''

        url="/api/v3/order"
        params={'symbol':symbol,'side':side,'type':type,'quantity':quantity,'price':price,'timestamp':utils.getTime()}
        if(newClientOrderId!=''):
            params.update({'newClientOrderId':newClientOrderId})
        if(stopPrice!=''):
            params.update({'stopPrice':stopPrice})
        if(icebergQty!=''):
            params.update({'icebergQty':icebergQty})
        if(timeInForce!=''):
            params.update({'timeInForce':timeInForce})
        
        data=self.hitBinanceWebAPI(self.POST, url, params,signed=True)
        return data
        
    def testNewOrder(self,symbol,side,type,quantity,price,timeInForce='', recvWindow='',newClientOrderId='',stopPrice='',icebergQty=''):
        '''
        Name                Type    Mandatory    Description
        symbol                STRING    YES    
        side                ENUM    YES    
        type                ENUM    YES    
        timeInForce            ENUM    YES    
        quantity            DECIMAL    YES    
        price                DECIMAL    YES    
        newClientOrderId    STRING    NO    A unique id for the order. Automatically generated if not sent.
        stopPrice            DECIMAL    NO    Used with stop orders
        icebergQty            DECIMAL    NO    Used with iceberg orders
        timestamp            LONG    YES    
        '''

        url="/api/v3/order/test"
        params={'symbol':symbol,'side':side,'type':type,'quantity':quantity,'price':price,'timestamp':utils.getTime()}
        if(newClientOrderId!=''):
            params.update({'newClientOrderId':newClientOrderId})
        if(stopPrice!=''):
            params.update({'stopPrice':stopPrice})
        if(icebergQty!=''):
            params.update({'icebergQty':icebergQty})
        if(recvWindow!=''):
            params.update({'recvWindow':recvWindow})
        if(timeInForce!=''):
            params.update({'timeInForce':timeInForce})
        
        data=self.hitBinanceWebAPI(self.POST, url,params,signed=True)
        return data
                
    def orderStatus(self,symbol,orderId='',origClientOrderId='',recvWindow=''):
        '''
        Name                Type    Mandatory    Description
        symbol                STRING    YES    
        orderId                LONG    NO    
        origClientOrderId    STRING    NO    
        newClientOrderId    STRING    NO            Used to uniquely identify this cancel. Automatically generated by default.
        recvWindow            LONG    NO    
        timestamp            LONG    YES    
        '''
        url="/api/v3/order"
        params={'symbol':symbol,'timestamp':utils.getTime()}
        if(origClientOrderId!=''):
            params.update({'origClientOrderId':origClientOrderId})
        if(orderId!=''):
            params.update({'orderId':orderId})
        if(recvWindow!=''):
            params.update({'recvWindow':recvWindow})
        
        
        data=self.hitBinanceWebAPI(self.GET, url,params,signed=True)
        
        return data
        
    def cancelOrder(self,symbol,orderId='',origClientOrderId='',newClientOrderId='',recvWindow=''):
        '''
        Name                Type    Mandatory    Description
        symbol                STRING    YES    
        orderId                LONG    NO    
        origClientOrderId    STRING    NO    
        newClientOrderId    STRING    NO    Used to uniquely identify this cancel. Automatically generated by default.
        recvWindow            LONG    NO    
        timestamp            LONG    YES    
        '''
        url="/api/v3/order"
        params={'symbol':symbol,'timestamp':utils.getTime()}
        if(origClientOrderId!=''):
            params.update({'origClientOrderId':origClientOrderId})
        if(orderId!=''):
            params.update({'orderId':orderId})
        if(recvWindow!=''):
            params.update({'recvWindow':recvWindow})
        if(newClientOrderId!=''):
            params.update({'newClientOrderId':newClientOrderId})
        
        data=self.hitBinanceWebAPI(self.DELETE, url,params,signed=True)
        
        return data
        
    def allOrders(self,symbol,recvWindow=''):
        '''
        Name        Type    Mandatory    Description
        symbol        STRING    YES    
        recvWindow    LONG    NO    
        timestamp    LONG    YES    
        '''
        
        url="/api/v3/allOrders"
        params={'symbol':symbol,'timestamp':utils.getTime()}
        
        if(recvWindow!=''):
            params.update({'recvWindow':recvWindow})
        
        data=self.hitBinanceWebAPI(self.GET, url,params,signed=True)
        
        return data
        
    def openOrders(self,symbol,recvWindow=''):
        '''
        Name        Type    Mandatory    Description
        symbol        STRING    YES    
        recvWindow    LONG    NO    
        timestamp    LONG    YES    
        '''
        url="/api/v3/openOrders"
        params={'symbol':symbol,'timestamp':utils.getTime()}
        if(recvWindow!=''):
            params.update({'recvWindow':recvWindow})
        
        data=self.hitBinanceWebAPI(self.GET, url,params,signed=True)
        
        return data
        
    def accountInfo(self):
        url="/api/v3/account"
        
        params={'timestamp':utils.getTime()}

        
        data=self.hitBinanceWebAPI(self.GET, url,params,signed=True)
        
        return data

    def accountTradesList(self,limit='',fromId='',recvWindow=''):
        '''
        
        Name        Type    Mandatory    Description
        symbol        STRING    YES    
        limit        INT        NO            Default 500; max 500.
        fromId        LONG    NO            TradeId to fetch from. Default gets most recent trades.
        recvWindow    LONG    NO    
        timestamp    LONG    YES    
        '''
        url="/api/v3/myTrades"
        params={'timestamp':utils.getTime()}
        data=self.hitBinanceWebAPI(self.GET, url,params,signed=True)
        
        return data

    
class WebSocketsAPI(threading.Thread):

    STREAM_URL = 'wss://stream.binance.com:9443/'

    WEBSOCKET_DEPTH_5 = '5'
    WEBSOCKET_DEPTH_10 = '10'
    WEBSOCKET_DEPTH_20 = '20'

    _user_timeout = 30 * 60  # 30 minutes
    
    def __init__(self):
        threading.Thread.__init__(self)
        self._conns = {}
        self._user_timer = None
        self._user_listen_key = None
        self._user_callback = None
        #self._client = client
        
    def startSocket(self,path,callback, prefix='ws/'):
        if path in self._conns:
            return False
        factory_url = self.STREAM_URL + prefix + path
        factory = protocols.BinanceClientFactory(factory_url)
        factory.protocol = protocols.BinanceClientProtocol
        factory.callback = callback
        factory.reconnect = True
        context_factory = ssl.ClientContextFactory()
        self._conns[path] = connectWS(factory, context_factory)
       
        return path
        
    def getListenKey(self):
        url="/api/v1/userDataStream"
        
            
        data=self.hitPostConnection(url)
        
        return data['listenKey']
        
    def keepAliveStream(self,listenKey):
        url="/api/v1/userDataStream"
        params={'listenKey':listenKey}
        data=self.hitPutConnection(url)
        
        return data
        
    def deleteStream(self,listenKey):    
        url="/api/v1/userDataStream"
        
        params={'listenKey':listenKey}
        data=self.hitDeleteConnection(url)
        
        return data

    def startTradeSocket(self, symbol, callback):
        return self.startSocket(symbol.lower() + '@trade', callback)
        
    def startKLineSocket(self, symbol,interval, callback):
        socketName = symbol.lower()+'@kline_'+interval
        return self.startSocket(symbol.lower(), callback)
    '''    
    def startTradeSocket(self, symbol,interval, callback):
        return self.startSocket(symbol.lower() + '@aggTrade', callback)
    '''

    def run(self):
        try:
            reactor.run(installSignalHandlers=False)
        except ReactorAlreadyRunning:
            # Ignore error about reactor already running
            pass

    def close(self):
        """Close all connections

        """
        keys = set(self._conns.keys())
        for key in keys:
            self.stop_socket(key)

        self._conns = {}
