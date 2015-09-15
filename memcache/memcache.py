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

import time
import math
import commands, sys
import logging
import uuid
from datetime import datetime, timedelta

keydict = {}
valdict = {}
ttldict = {}

class memcache():
	
#	keydict = {}
#       valdict = {}
#        ttldict = {}
		
	def put(self, key, val, ttl):
		#logging.info ("Key :"+ key +" Value :"+ str(val)+" TTL :"+ttl)
		global keydict
		global valdict
		global ttldict
		if key in keydict.keys():
                        uid = keydict[key]
                else:
                        uid = self.genid()
			keydict[key] = uid
		
		valdict[uid] = val
		# if ttl = -1 this means that we need to ignore ttl
		if ttl != -1:
			#DATETIME_FORMAT='%Y-%m-%dT%H:%M:%S'
                        #ttltimme = datetime.datetime.strptime(resauth['valid_from'],DATETIME_FORMAT)
			# get convert the ttl into a time value and store it
			ttltime = datetime.now()+timedelta(seconds=ttl)
			ttldict[uid] = ttltime
			logging.info("Setting TTL Expiry to: "+ str(ttltime))
			logging.info('Internal uid :' + str(uid))	
	def get(self, key):
		global keydict
		global valdict
		global ttldict
		logging.info("Getting value for key " + key)
		if key in keydict.keys():
			idval = keydict[key]
		else:
			logging.info('Returning null')
			return {}
		
		value = valdict[idval]
		logging.debug('Value for key '+ str(value))
		logging.debug('Retreiving TTL value for :'+str(idval))
		if idval in ttldict.keys():
			ttlvalue = ttldict[idval]
			logging.info('TTL Expiry :' + str(ttlvalue))
			#logging.info('Retreiving TTL value for :'+idval)
			# check if ttl value is valid here TBD
			DATETIME_FORMAT='%Y-%m-%dT%H:%M:%S'
                        #ttltimme = datetime.strptime(ttlvalue, DATETIME_FORMAT)
			logging.info('Comparing TTL with '+ datetime.now())
			if ttlvalue > datetime.now():
				logging.info('TTL expired. Deleting key and val from cache')
				del valdict[idval]
				del ttldict[idval]
				del keydict[key]
				return {}
			return {'key' : key , 'value' : value , 'ttl' : ttlvalue }
		return {'key' : key , 'value' : value }

	def genid(self):
		return uuid.uuid4()

	def keys(self):
		return keydict.keys()
	
	def purge(self):
		logging.info('Purging the whole cache')
		global keydict
                global valdict
                global ttldict
		keydict.clear()
		valdict.clear()
		ttldict.clear()
