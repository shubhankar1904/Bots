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
 

from credentials import *    # This will allow us to use the keys as variables

#Below is spark session instance. Hive server details present in hive-site.xml in conf folder of spark installation
spark = SparkSession \
                .builder \
                .appName("ALT_COIN_HIST_DATA")\
                .config("spark.sql.hive.metastore.sharedPrefixes","com.mysql.jdbc")\
                .config("spark.sql.hive.metastore.jars","builtin")\
                .enableHiveSupport()\
                .getOrCreate()


    
    
    
    def on_status(self, status):
        cleanTweet =  clean_tweet(status.text)
        sam = analize_sentiment(cleanTweet)
        
        coins = getCoin(cleanTweet)
#       
        if sam != 0:
            
            coins = getCoin(cleanTweet)
            
            for coin in coins:
                row = (str(cleanTweet),\
                           str(coin),\
                           "Binance", \
                            float(round(float(sam),5)),\
                            int(status.created_at.year),\
                            int(status.created_at.month),\
                            int(status.created_at.day),\
                            int(status.created_at.hour),\
                            int(status.created_at.minute),\
                            int(status.created_at.second),\
                            str(datetime.datetime.now()))
                self.rows.append(row)
                print len(self.rows)
            
            if(len(self.rows) % 1000 == 0 ):
                print "Appendig Rows"
               
                rdd = spark.sparkContext.parallelize(self.rows)
                tweets = rdd.map(lambda x: Row(tweet=x[0], coin=x[1],\
                                               exchange=x[2], sentiment=x[3],\
                                               year=x[4], month=x[5],\
                                               day=x[6], hour=x[7],\
                                               min=x[8], sec=x[9],\
                                               timestamp = x[10]
                                               
                                               ))
                recordsDF = spark.createDataFrame(tweets,schema)
                recordsDF.registerTempTable("tweets")
                recordsDF.write.format('hive').mode("append").saveAsTable("twitter_data")
                


#spark.sql(" DROP TABLE IF EXISTS twitter_data")
spark.sql("CREATE TABLE IF NOT EXISTS coins_data (tweet string, coin string, exchange string, sentiment float, year int, month int, day int, hour int, min int, sec int, timestamp string)")

schema= StructType([StructField("tweet", StringType(), True),\
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



extractor = twitter_setup()
                
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = extractor.auth, listener=myStreamListener)




while(True):
    try:        
        myStream.filter(track=binance_coin_list.coin_list, async=True)
        print "retrying"
    except tweepy.TweepError as e:
        
        continue
    