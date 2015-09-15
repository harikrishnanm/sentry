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
#from db import keycheck
import datetime
import logging

#+---------+-------------+------+-----+---------+----------------+
#| Field   | Type        | Null | Key | Default | Extra          |
#+---------+-------------+------+-----+---------+----------------+
#| udid    | int(11)     | NO   | PRI | NULL    | auto_increment |
#| userkey | varchar(8)  | YES  | MUL | NULL    |                |
#| imei    | varchar(50) | YES  |     | NULL    |                |
#| imsi    | varchar(50) | YES  |     | NULL    |                |
#+---------+-------------+------+-----+---------+----------------+



class auth:
#	def main():
		
#	def __init__(self):

#		pass

	def getdb(self):
        	try:
                	con = mdb.connect('localhost', 'root', 'root123', 'sentry');
                	#cur = con.cursor()                	
			return con
                	#cur.execute("SELECT passkey, name, valid_from, valid_to from u$
                	#res= cur.fetchone()
                	#print res[0]
        	except mdb.Error, e:
                	print "Esddsrror %d: %s" % (e.args[0],e.args[1])
                #finally:
                #	if con:
                #        	con.close()

	def checkauth(self, imei, imsi, key):
        	#logging.info( "In checkauth")
		logging.basicConfig(filename='/var/log/sentry1.log',format='%(asctime)s pid:%(process)s module:%(module)s %(message)s', level=logging.DEBUG)
		db = self.getdb()
		cur = db.cursor()
		#kc = keycheck()
		
		logging.info("Generating cache key")

		cachekey = key + imei + imsi
		logging.info("Cache key: "+ cachekey)
		#memc = memcache.Client(['127.0.0.1:11211'])
		cachedata = ''
		if  not cachedata:
			logging.info("No Cache hit. Getting from DB")
			db = self.getdb()
                	cur = db.cursor()
			sql = "select user.username, user.email, user.name, user.phone, user.password, user.valid_to, user.valid_from "
			sql += "from user, user_device where user.passkey = user_device.passkey and user_device.passkey = '"
			sql += key
			sql += "\' and user_device.imei = \'"
			sql += imei
			sql += "\' and user_device.imsi = \'"
			sql += imsi
			sql += "\'"
			logging.debug(sql)
		# check key validity as well.
			
			cur.execute(sql)
			devauth = cur.fetchone()
			logging.info(devauth[0])
			logging.info(devauth[1])
			cur.close()
			del cur
		#	db.close()
		#	keyauth = kc.checkKey(key)
			#logging.info("Keyauth: "+ keyauth)
		#	now = datetime.datetime.now()
		#	if devauth != None and keyauth !=0 and keyauth['valid_from'] < now and keyauth['valid_to'] > now :
		#		#if devauth != None:
		
#		return 1

#			else:
#				return 0
		else:
			logging.info("Cache hit")
		# get the data from the cache here. 

	def main():
		checkauth('359359054792061','404450116132737','1975')

if __name__ == "__main__":
        auth().checkauth('359359054792061','404450116132737','1975')




