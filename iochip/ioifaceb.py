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
import logging

class ioifaceb:
	
	address = 0x27 # Default I2C address of MCP23017
	port_a_dir = 0x00 # GPIOA Direction
	 # GPIOB Direction

	port_a_address = 0x12
	port_b_address = 0x13
	UNLOCK_DURATION = 2

	port_b_regs = [0x01,0x03,0x07,0x09,0x0b,0x0d,0x05]
	port_b_vals = [0xf0, # w 0-3 0-R1 1-R2 r 4-7 4-ExSw 5-EM1 6-EM2
               0xff, # Input polarity non inverted
               0x00, # DEFVAL register for interrupt
               0xfe, # all
               0x02, # Set interrupt polarity to high
               0xff, # enable internal pullups
               0xfe  # set GPINTENB to enable interrupt
               ]

	
	def __init__(self):
		"Intialize port A and then B"
#		global bus
		self.iobus = smbus.SMBus(1)
	        logging.info(self.initialize('A'))
	        logging.info(self.initialize('B'))
		self.DEF_LOCKED = 1
		self.DEF_UNLOCKED = 0

	def reinit(self):
		logging.info(self.initialize('A'))
                logging.info(self.initialize('B'))
		
	def initialize(self, port):
		"Initialize the IO Chip. Port A is output to consolelcd Port B is for sensors and relay"
		if port =='A':
	                self.writedata(self.port_a_dir, 0x00)
        	        return [1,'Port A initialized']
	        elif port == 'B':
        	        for reg, val in zip(self.port_b_regs, self.port_b_vals):
                		self.writedata(reg,val)
	                return [1,'Port B initialized']
        	else:
                	return [-1,'Undefined port']

	def writedata(self, register, val):
        	self.iobus.write_byte_data(self.address, register, val)
		
	def getbus(self):
		return self.iobus

	def unlock(self):
		self.setlockstate(self.DEF_UNLOCKED)
		time.sleep(self.UNLOCK_DURATION)
		self.setlockstate(self.DEF_LOCKED)

	def open(self):
		self.setlockstate(self.DEF_UNLOCKED)
	
	def close(self):
		delf.setlockstate(self.DEF_LOCKED)

	def openshut(self):
		self.setlockstate(self.DEF_UNLOCKED)
		time.sleep(self.UNLOCK_DURATION)
		self.setlockstate(self.DEF_LOCKED)

	def keepopen(self):
		self.setlockstate(self.DEF_UNLOCKED)

	def lock(self):
		self.setlockstate(self.DEF_LOCKED)
		
	def setlockstate(self, state):
 
		#datalock = 0x00
		#$dataunlock = id & 0x0f
		#print dataunlock
		LOCK_BITS = 0x0f
		UNLOCK_BITS = 0x00
		if state == 1:
			logging.info("Engaging EM Locks")
			self.iobus.write_byte_data(self.address, self.port_b_address, LOCK_BITS)
		elif state == 0:
			logging.info("Disengaging EM Locks")
			self.iobus.write_byte_data(self.address, self.port_b_address,UNLOCK_BITS)

