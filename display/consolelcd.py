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

# Created on Jul 31, 2013
# @author: Hari

import consolelcdhelper
import datetime
import time

class consolelcd:

	default_text = ".BOOTING SENTRY."
	def __init__(self, iobus):
		"Initiate the helper"
		self.iobus = iobus
	
	def initialize(self):
		self.dishelper = consolelcdhelper.consolelcdhelper(self.iobus)
		self.dishelper.initialize()

	
	def clear(self):
		self.dishelper.clear()

	def setsensormsg(self, msg):
		#self.clear()
		self.setline(2)
		self.dishelper.setmessage(msg)
	
	def overridesensormsg(self, msg):
		self.setline(2)
		self.dishelper.setmessage(msg)
		time.sleep(1)

	def setsystemmsg(self, msg):
		self.setline(1)
		self.dishelper.setmessage(msg)

	def setline(self, line):
		self.dishelper.setline(line)

	def writemaskedchar(self, key):
		self.dishelper.writemaskedchar(key)
		
	def setdefault(self):
		#First line is default text
		self.clear()
		str_def = self.default_text.center(16,' ')
                for i in range(0, len(str_def)):
                        self.dishelper.writelcdchar(str_def[i])
               # self.updatetime() # update the time
	if __name__ == '__main__':
       		initialize()

