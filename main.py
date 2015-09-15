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

from iochip import ioifacea
from iochip import ioifaceb
from display import lcd, timeupdate, consolelcd
from monitor import monitorsensors, sysmonitor
from rpc import sentryproxy
from memcache import memcache, memcachemgr
from db import dbstatemgr
from system import pycommands
from keypad import keypad

import Pyro4

import threading
import logging
import signal 
import sys
import shutil
import os

#Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.HMAC_KEY = '12345'
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
cache = memcache()

DB_FILE_SAVED = '/home/pi/sentry/sentry/db/sqlite/sentry_save.db'
DB_FILE_BOOTSTRAP = '/home/pi/sentry/sentry/db/sqlite/sentry_bootstrap.db'
DB_FILE_ACTIVE = '/var/tmp/sentry.db' # in memory file system
def main():
	global daemon
	global cache
	
	logging.basicConfig(filename='/var/log/sentry.log',format='%(asctime)s pid:%(process)s module:%(module)s %(message)s', level=logging.DEBUG)
	logging.info("Starting the main program threads")	
	
	signal.signal(signal.SIGINT, exithandler)
	
	lock = threading.Lock()
	lock1 = threading.Lock()
	
	logging.info("Initializing Filesystem")
	cmdutil =pycommands()
	cmdutil.mountro()

	logging.info("Starting cache monitor thread")
        cachemanager = memcachemgr()
        cachemanager.daemon = True
#        cachemanager.start()

	logging.info('Initializing DB')
	dbstatemgrthread = dbstatemgr(cachemanager)
	dbstatemgrthread.daemon = True
	dbstatemgrthread.start()
	#initialize io chip
	try:
		logging.info("Intializing the IO chip A")
		ioc = ioifacea()
		iobus = ioc.getbus()
		logging.info("Initializing the Keypad Display")
        	# Initiate the display and set th default message
       		dis = lcd(iobus)
        	dis.initialize()
        	dis.setdefault()
	except IOError, e:
		logging.error("IO chip A is not initialized. Keypad functions will not be available")
		#logging.error(e.errno)
		logging.error(e)	
		
	try:	
		logging.info("Initializing the IO chip B")
		iocb = ioifaceb()
		iobusb = iocb.getbus()
	except IOError, e:
                logging.error("IO chip B is not initialized. EM functions will not be available")
                #logging.error(e.errno)
                logging.error(e)

	logging.info("Setting EM relays to locked state")
	iocb.lock()
	
	logging.info("Initializing the Console Display")
	consoledis = consolelcd(iobusb)
	consoledis.initialize()
	#consoledis.setdefault()
	
	#logging.info("Initializing the Keypad Display")
	# Initiate the display and set th default message
	#dis = lcd(iobus)
	#dis.initialize()
	#dis.setdefault()
	
	logging.info("Initializing the system monitor thread")
	sysmonthread = sysmonitor(iobusb, consoledis, lock)
	sysmonthread.daemon = True
	sysmonthread.start()
	
	logging.info("Initializing the sensor monitor thread")
	monitorthread = monitorsensors(iocb, iobusb, consoledis, lock)
	monitorthread.daemon = True
	monitorthread.start()
	
	#logging.info("Starting time update thread")
	#timeupdatethread = timeupdate(dis,lock1)
	#timeupdatethread.daemon = True
	#timeupdatethread.start()
	
	#logging.info("Starting key scanner")
	#keyscanner = keypad(iocb, iobus, iobusb, dis, consoledis, timeupdatethread, monitorthread, lock1)
	#keyscanner.daemon = True
	#keyscanner.start()

	'Initiating RPC client'
	sproxy = sentryproxy(lock)

	ns = Pyro4.locateNS()
	
	logging.info("Starting RPC server daemon")
	daemon = Pyro4.core.Daemon(host="127.0.0.1")
	
	logging.info("Registering objects with RPC")
	#tuturi = daemon.register(timeupdatethread)
	#ns.register('sentry.timeupdatethread', tuturi)
	
	logging.info("Registering cache object with RPC")
	cacheuri = daemon.register(cache)
	ns.register('sentry.cache', cacheuri)
	cachemanager.start()

	logging.info("Registering sensor monitor with RPC")
	monuri = daemon.register(monitorthread)
	ns.register('sentry.sensormonitor', monuri)
	
	#iocuri = daemon.register(ioc)
	#ns.register('sentry.ioc', iocuri)

	iocburi = daemon.register(iocb)
	ns.register('sentry.iocb', iocburi)
	
	#disuri = daemon.register(dis)
	#ns.register('sentry.dis', disuri)
	
	consoledisuri = daemon.register(consoledis)
	ns.register('sentry.consoledis', consoledisuri)

	sentryproxyuri = daemon.register(sproxy)
	ns.register('sentry.proxy', sentryproxyuri)
	logging.info("Starting RPC poll loop")
	
	daemon.requestLoop()	

def exithandler(signal, frame):
	# do whatever here
	global daemon
	daemon.shutdown()



if __name__ == "__main__":
    	main()
