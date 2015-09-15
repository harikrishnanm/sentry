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

import lcdhelper
import datetime

class lcd:

	default_text = "KRISHNANS"
	def __init__(self, iobus):
		"Initiate the helper"
		self.iobus = iobus
	
	def initialize(self):
		self.dishelper = lcdhelper.lcdhelper(self.iobus)
		self.dishelper.initialize()
	
	def clear(self):
		self.dishelper.clear()

	def setmessage(self, msg):
		self.dishelper.setmessage(msg)

	def setline(self):
		self.dishelper.setline()

	def writemaskedchar(self, key):
		self.dishelper.writemaskedchar(key)

	def setmessage2(self, msg):
		self.dishelper.setline()
		self.dishelper.setmessage2(msg)

	def setdefault(self):
		#First line is default text
		self.clear()
		str_def = self.default_text.center(16,' ')
                for i in range(0, len(str_def)):
                        self.dishelper.writelcdchar(str_def[i])
                self.updatetime() # update the time
                
	def updatetime(self):
#		print "Updating time"
		localtime = datetime.datetime.now().strftime("%H:%M:%S %d %b")
		self.dishelper.setline()
                str_def = localtime.center(16,' ')
                for j in range(0,len(str_def)):
                        char1 = str_def[j]
                        self.dishelper.writelcdchar(char1)

	if __name__ == '__main__':
       		initialize()

