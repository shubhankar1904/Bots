import requests
import time
import datetime
import config
import hmac
import hashlib
import base64

	
	
	
def getQueryString(param):
	
	queryString=''
	print param
	for parameters in param:
	
		queryString = queryString + str(parameters) + "=" + str(param[parameters]) +"&"
	
	return queryString[:-1]
	
def getTime():
	return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)-1000
	
def getSignature(msg):
	return hmac.new(config.getSecretKey().encode('utf-8'), msg=msg.encode('utf-8'), digestmod=hashlib.sha256).hexdigest();
	
