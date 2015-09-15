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

import smbus
import sys
import getopt
import time
import collections
import io
import datetime
import thread
import threading
import logging
# This class has all the methods to initialize and send data to the lcd


class consolelcdhelper:
	
	def __init__(self, iobus):
		self.iobus = iobus
		self.address = 0x27 # I2C address of MCP23017
		self.port = 0x12 # GPIOA
        	self.en_port_mask = 0xf0
	        self.init_vals = [0x32, 0x32, 0x32, #Intialization
        		0x22, # Enter 4 bit mode
		        0x22, 0x82, # default was 28 2nd byte
		        0x02, 0x82, # default was 08
		        0x02, 0x12, # default was 01 Clear display
		        0x02, 0x62, # default as 06
		        0x02, 0xc2 # Bits 11CB
		        ]

		self.clearcmd = [0x02, 0x00, 0x12, 0x10]
		#self.clearcmd = []
		self.setl2cmd = [0xc2, 0xc0, 0x02, 0x10]
		self.setl1cmd = [0x82, 0x80, 0x02, 0x10]
		self.curshiftrcmd = [0x12, 0x10, 0x42, 0x40]
		self.curshiftlcmd = [0x12, 0x10, 0x02, 0x00]

		self.delay_dur = .001 #s
		self.char_mode_bit ='3'
		self.cmd_mode_bit = '2'

	def initialize(self):
        	#logging.info("Initialize the Console LCD")
#	        iochip.initialize('A') # just in case its not initialzed.
        	splitmask = False # set this for initialization
	        for val in self.init_vals:
	                self.writelcdcmd(val, splitmask)
        	#logging.info("Console LCD initalized")
		
	def splitbyte(self, bytein, mode_bits):
        	h, l = divmod(ord(bytein),16)
	        # Add the char mode bits
        	h1 = hex(h) + mode_bits
	        l1 = hex(l) + mode_bits
        	hval = int(hex(int(h1,16)),16)
        	lval = int(hex(int(l1,16)),16)
	        return hval, lval

	def writelcdcmd(self, val, splitmask):
	        if splitmask == True:
        	        # split into two
                	x, y = self.splitbyte(val, self.cmd_mode_bit)
	                # now write the two bytes
        	        self.writelcddata(x)
                	self.writelcddata(y)
        	else:
                	self.writelcddata(val)

	def writelcdchar(self, chrasc):
	        #Split the bits
        	hval, lval = self.splitbyte(chrasc, self.char_mode_bit)
		#       print hval,lval
	        self.writelcddata(hval)
        	self.writelcddata(lval)

	def writelcddata(self, val):
		self.iobus.write_byte_data(self.address, self.port, val)
        	# and Toggle enable
	        self.iobus.write_byte_data(self.address, self.port, self.en_port_mask)
		self.delay(.005)
		#lock.release()

	def delay(self, duration=.01):
	#       print duration
        	time.sleep(duration)
	
	def setmessage(self, msg):
		#self.clear()
	#	self.setline()
		str_def = msg.ljust(16,' ')
        	for i in range(0, len(str_def)):
        		self.writelcdchar(str_def[i])

	def writemaskedchar(self, val):
		# display char for some timm
		#self.writelcdchar(val[0]) # just in case the length is > 1 only display first char
		#self.delay(.09)
		# move cursor left
		#self.curshiftleft()
		self.writelcdchar('*')
		# curshiftright()

	def clear(self):
		for val in self.clearcmd:
                        self.writelcdcmd(val, False)
        	self.delay(.005)

	def setline(self, line):
		if line == 1:
			for val in self.setl1cmd:
        	                self.writelcdcmd(val, False)

		elif line == 2:
			for val in self.setl2cmd:
				self.writelcdcmd(val, False)
	        self.delay(.1)

	def curshiftleft(self):
        	for val in self.curshiftlcmd:
                        self.writelcdcmd(val, False)
                self.delay(.002)

	def curshiftright(self):
	        for val in self.curshiftrcmd:
                        self.writelcdcmd(val, False)
                self.delay(.002)
