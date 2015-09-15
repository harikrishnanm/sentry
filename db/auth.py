#   Sentry
#
#   This file is part of Sentry
#
#   Sentry is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Sentry is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
#   @copyright Copyright Harikrishnan M <harkrishnanm@gmail.com>
#   @licence GNU Public License V3.0
#
#
#!/usr/bin/python

import MySQLdb as mdb
import sys
from db import keycheck
import datetime
import logging
import memcache
import Pyro4
import sqlite3 as lite

#+---------+-------------+------+-----+---------+----------------+
#| Field   | Type        | Null | Key | Default | Extra          |
#+---------+-------------+------+-----+---------+----------------+
#| udid    | int(11)     | NO   | PRI | NULL    | auto_increment |
#| userkey | varchar(8)  | YES  | MUL | NULL    |                |
#| imei    | varchar(50) | YES  |     | NULL    |                |
#| imsi    | varchar(50) | YES  |     | NULL    |                |
#+---------+-------------+------+-----+---------+----------------+


Pyro4.config.HMAC_KEY = '12345'

class auth:
	def __init__(self):
		pass

	def getdb(self):
        	try:
                	logging.debug('Connecting to the Database')
			#con = mdb.connect('localhost', 'root', 'root123', 'sentry');
                	con = lite.connect('/var/tmp/sentry.db')
			#cur = con.cursor()
			if con != None:                	
				return con
			else:
				logging.debug("Error getting database connection")
				
                	#cur.execute("SELECT passkey, name, valid_from, valid_to from u$
                	#res= cur.fetchone()
                	#print res[0]
        	except mdb.Error, e:
                	logging.debug( "ERROR")
                #finally:
                #	if con:
                #        	con.close()

	def checkauth(self, imei, imsi, key):
        	logging.debug( "In checkauth")
		#db = self.getdb()
		#cur = db.cursor()
		#kc = keycheck()
		ns = Pyro4.naming.locateNS()
                cache = Pyro4.Proxy("PYRONAME:sentry.cache")
                cachekey = imei+imsi+key
		logging.info("IMEI: " +imei)
		logging.info("IMSI: " +imsi)
		logging.info("KEY: " +key) 
		logging.info("Cache key :" +cachekey)
		cachehit = 0
		if cachekey in cache.keys():
			#Cache hit
			logging.info("Cache Hit")
			cachehit = 1
			# get the data from the cache
			resauth = cache.get(cachekey).get('value')
			logging.debug("Cache Key = "+ cachekey)
			#logging.debug("Cache Value = "+ str(resauth))
		else:
			logging.info("Cache Miss")
			db = self.getdb()
                	cur = db.cursor()
                	kc = keycheck()			
			sql = "select * from user_device where passkey = \'"
			sql += key
			if imei != 'web' and imsi != 'web':
				sql += "\' and imei = \'"
				sql += imei
				sql += "\' and imsi = \'"
				sql += imsi
			sql += "\'"
			logging.debug(sql)
			# check key validity as well.
			cur.execute(sql)
			devauth = cur.fetchone()
			logging.debug('Fetched data')
			resauth = {}
			if devauth != None:
				resauth['udid'] = devauth[0]
				resauth['userkey'] = devauth[1]
				resauth['imei'] = imei #devauth[2]
				resauth['imsi'] = imsi #devauth[3]
				#cur.close()
				#del cur
				#db.close()
				keyauth = kc.checkKey(key)
				resauth['valid_from'] = keyauth['valid_from']
				resauth['valid_to'] = keyauth['valid_to']
			cache.put(cachekey, resauth, -1)
			logging.debug("Added result to cache")
			cur.close()
                        del cur
                        db.close()			
			#logging.debug("Added result to cache")

		if resauth != None and 'udid' in resauth.keys() and resauth['udid'] != '':
			# authenticated. Now check validity
			logging.debug('Authenticated. Now check Validity')
                        retval = 2
			now = datetime.datetime.now()
			DATETIME_FORMAT='%Y-%m-%d %H:%M:%S'
			#if cachehit == 1:
			logging.debug('Converting date from unicode to datetime')
			validfrom = datetime.datetime.strptime(resauth['valid_from'],DATETIME_FORMAT)
			validto = datetime.datetime.strptime(resauth['valid_to'],DATETIME_FORMAT)
			#else:
			#	logging.debug('Comparing dateime directly')
			#	validfrom = resauth['valid_from']
			#	validto = resauth['valid_to']
                        if validfrom < now and validto > now:
                        	retval = 1
		else:
                	retval = 0
              	return retval
