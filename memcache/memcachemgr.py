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
import Pyro4
import threading
import time
import logging
import memcache

from datetime import datetime

class memcachemgr(threading.Thread):
	
	def __init__(self):
                logging.info("Initializing Cache manager")
		threading.Thread.__init__(self)
	
	def run(self):
		logging.info('Starting the cachemgr thread run')
		self.clearcache()
	
	def clearcache(self):
		while(True):
			logging.info('Clearing cache')
			ns = Pyro4.naming.locateNS()
                	cache = Pyro4.Proxy("PYRONAME:sentry.cache")
			cache.purge()
			now = datetime.now()
			seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
			seconds_to_clear = 86400 - seconds_since_midnight + 518400 #clear once a week
			logging.info('Next cache clear in '+str(seconds_to_clear)+' seconds')
			time.sleep(seconds_to_clear)
	
	def clearcacheimd(self):
			logging.info('Clearing cache immediate')
                        ns = Pyro4.naming.locateNS()
                        cache = Pyro4.Proxy("PYRONAME:sentry.cache")
                        cache.purge()

