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

import Pyro4
import time
from db import auth,dbutil,keycheck
import datetime
import logging
from gcmclient import gcmhelper

class sentryproxy:

	def __init__(self, lock):
		self.lock = lock
		ns=Pyro4.naming.locateNS()
		self.ioifaceb = Pyro4.Proxy("PYRONAME:sentry.iocb")
		self.sensormon = Pyro4.Proxy("PYRONAME:sentry.sensormonitor")
        	self.consoledis = Pyro4.Proxy("PYRONAME:sentry.consoledis")        
		self.DEF_LOCKED = 1
		self.DEF_UNLOCKED = 0

	def authdev(self, imei, imsi, key):
		#print "Checkauth IMEI:" + imei + " IMSI:"+imsi
		dbauth = auth()
		self.key = key
		#print "Got dbauth instance"
		return dbauth.checkauth(imei, imsi, key)
			

	def lock(self):
		logging.info("Locking")
		self.sensormon.setactive(False)
		self.ioifaceb.lock()
		self.consoledis.setsensormsg("REQUEST: LOCK")
		time.sleep(2)
                self.sensormon.setactive(True)


	def unlock(self):
		print "here"
                logging.info("Unlocking")
		self.sensormon.setactive(False)
		#self.ioifaceb.unlock()
                self.lock.acquire()
		self.consoledis.setsensormsg("REQUEST: UNLOCK")
		self.ioifaceb.unlock()
		self.lock.release()
		self.sensormon.setactive(True)
		self.sendnotification(self.key)

	def keepopen(self):
		logging.info("Keep Open")
		self.sensormon.setactive(False)
                #self.ioifaceb.unlock()
                self.lock.acquire()
                self.consoledis.setsensormsg("REQUEST: KEEP-OPEN")
                self.ioifaceb.keepopen()
                self.lock.release()
                self.sensormon.setactive(True)
                self.sendnotification(self.key)

	def addregid(self, regid):
		logging.info("Adding Regid" + regid)
		dbut = dbutil()
		dbut.addregid(regid)
	

	def sendnotification(self, key):
		kc = keycheck()
		result = kc.checkKey(key)
		ltime = datetime.datetime.now().strftime("%a, %b %H:%M")
                data = {'MSG': 'Unlocked-Phone','USER': result['name'], 'TIME': ltime}
		gcmhelp = gcmhelper()
                gcmhelp.sendgcmsg(data, -1)
		#data = {'MSG': 'Unlocked from phone', 'USER': result['name'], 'TIME': ltime}	
                #gcmhelp = gcmhelper()
                #gcmhelp.sendgcmsg(data)
	
	def getstate(self):
		return self.sensormon.getstate()

def main():
	sproxy = sentryproxy()
	sproxy.unlock()
	sproxy.lock()
		
if __name__ == "__main__":
       	main()
