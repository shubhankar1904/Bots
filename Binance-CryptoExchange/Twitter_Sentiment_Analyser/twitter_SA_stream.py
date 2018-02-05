import tweepy           # To consume Twitter's API
import datetime
from textblob import TextBlob
import re
import sys
import findspark
from requests.exceptions import ConnectionError
findspark.init()
from pyspark import HiveContext,SparkContext
from pyspark.sql import SparkSession,Row
from pyspark.sql.types import *
import pyspark
import binance_coin_list 
import time
import pymysql


from credentials import *    # This will allow us to use the keys as variables

#Below is spark session instance. Hive server details present in hive-site.xml in conf folder of spark installation
'''
spark = SparkSession \
                .builder \
                .appName("Twitter_SA_Engine")\
                .config("spark.sql.hive.metastore.sharedPrefixes","com.mysql.jdbc")\
                .config("spark.sql.hive.metastore.jars","builtin")\
                .enableHiveSupport()\
                .getOrCreate()
'''                

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='coin_data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()        
cursor.execute("CREATE TABLE if not exists twitter_data (tweet VARCHAR(300), coin VARCHAR(5), exchange VARCHAR(10), sentiment float(8,7), createdat datetime, ts timestamp);")
connection.commit()
       
                
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return analysis.sentiment.polarity
    elif analysis.sentiment.polarity == 0:
        return analysis.sentiment.polarity
    else:
        return analysis.sentiment.polarity
        
def getCoin(tweet):
    coins=[]
    words = [word for word in tweet.split() if len(word) == 3 or len(word) == 4]
    for word in words:
        if(word.upper() in binance_coin_list.coin_list and word.upper() not in coins):
            coins.append(word.upper())
    return coins        
    
def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    print CONSUMER_KEY
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api



class MyStreamListener(tweepy.StreamListener):
    rows=[]
    
    def on_timeout(self):
        raise Exception("TimedOut. Reconnecting")
    
    def on_status(self, status):
        cleanTweet =  clean_tweet(status.text)
        sam = analize_sentiment(cleanTweet)
        
        coins = getCoin(cleanTweet)
#       
        if sam != 0:
            
            coins = getCoin(cleanTweet)
            print cleanTweet
            for coin in coins:
                
                sql = "INSERT INTO `titter_data` (`tweet`, `coin`,'exchange','sentiment',\
                'createdat','ts') VALUES (%s, %s, %s, %s, %s)"
                
                cursor.execute(sql, (     str(cleanTweet),\
                            str(coin),\
                            "Binance", \
                            float(round(float(sam),5)),\
                            (status.created_at),\
                            (datetime.datetime.now()),\
                            ))
                connection.commit()
  
                #print status.created_at
                #print datetime.datetime.now()
                #print len(self.rows)
            
            if(len(self.rows) % 1000 == 0 ):
                print "committing"
                connection.commit()


'''

class MyStreamListener(tweepy.StreamListener):
    rows=[]
    
    def on_timeout(self):
        raise Exception("TimedOut. Reconnecting")
    
    def on_status(self, status):
        cleanTweet =  clean_tweet(status.text)
        sam = analize_sentiment(cleanTweet)
        
        coins = getCoin(cleanTweet)
#       
        if sam != 0:
            
            coins = getCoin(cleanTweet)
            # print cleanTweet
            for coin in coins:
                row = (     str(cleanTweet),\
                            str(coin),\
                            "Binance", \
                            float(round(float(sam),5)),\
                            int(status.created_at.year),\
                            int(status.created_at.month),\
                            int(status.created_at.day),\
                            int(status.created_at.hour),\
                            int(status.created_at.minute),\
                            int(status.created_at.second),\
                            str(datetime.datetime.now()),\
                            )
                self.rows.append(row)
                #print status.created_at
                #print datetime.datetime.now()
                #print len(self.rows)
            
            if(len(self.rows) % 1000 == 0 ):
                print "Appendig Rows"
               
                rdd = spark.sparkContext.parallelize(self.rows)
                tweets = rdd.map(lambda x: Row( tweet=x[0], coin=x[1],\
                                               exchange=x[2], sentiment=x[3],\
                                               year=x[4], month=x[5],\
                                               day=x[6], hour=x[7],\
                                               min=x[8], sec=x[9],\
                                               timestamp = x[10]\
                                               
                                               
                                               ))
                recordsDF = spark.createDataFrame(tweets,schema).dropDuplicates()
                recordsDF.registerTempTable("tweets")
                recordsDF.write.format('hive').mode("append").saveAsTable("twitter_data")
                

'''


'''
#spark.sql(" DROP TABLE IF EXISTS twitter_data")
spark.sql("CREATE TABLE IF NOT EXISTS twitter_data (tweet string, coin string, exchange string, sentiment float, year int, month int, day int, hour int, min int, sec int, timestamp string)")

schema= StructType(  [ StructField("tweet", StringType(), True),\
 StructField("coin", StringType(), True),\
 StructField("exchange", StringType(), True),\
 StructField("sentiment", FloatType(), True),\
 StructField("year",IntegerType(), True),\
 StructField("month",IntegerType(), True),\
 StructField("day",IntegerType(), True),\
 StructField("hour",IntegerType(), True),\
 StructField("min",IntegerType(), True),\
 StructField("sec",IntegerType(), True),\
  StructField("timestamp",StringType(), True),])


recordsDF = spark.createDataFrame([],schema)
recordsDF.createOrReplaceTempView("tweets")
recordsDF.registerTempTable("twitter_data") 

'''

extractor = twitter_setup()
                
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = extractor.auth, listener=myStreamListener)




while(True):
    try:        
        myStream.filter(track=binance_coin_list.coin_list, async=True)
        print "retrying"
    except tweepy.TweepError as e:
        
        continue