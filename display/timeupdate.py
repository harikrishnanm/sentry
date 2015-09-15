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

import threading
import time
import lcd


exitFlag = 0
delay = 1

class timeupdate(threading.Thread):
	displayFlag = 1
	def __init__(self, dis, lock):
        	threading.Thread.__init__(self) # super ini
	        self.dis = dis
		self.lock = lock
		counter = 5
	
	def run(self):
	        self.updatetime(self.dis)
	
	def setDisplayFlag(self, state):
		self.displayFlag = state

	def updatetime(self, dis):
		while (True):
			#print self.displayFlag
			if self.displayFlag == 1:
				self.lock.acquire()
				dis.updatetime()
				self.lock.release()	
			time.sleep(delay)
