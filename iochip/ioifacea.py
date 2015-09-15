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

class ioifacea:
	
	address = 0x20 # Default I2C address of MCP23017
	port_a_dir = 0x00 # GPIOA Direction
	port_b_dir = 0x01 # GPIOB Direction

	port_a_address = 0x12
	port_b_address = 0x13
	
	port_b_regs = [0x01,0x03,0x07,0x09,0x0b,0x0d,0x05]
	port_b_vals = [0x1f, # read bits 0-4
               0x00, # Input polarity non inverted
               0x0f, # DEFVAL register for interrupt
               0x1f, # Compare bits 0-3 against defval 1 4 against defval 0
               0x02, # Set interrupt polarity to high
               0x0f, # Enable internal pullups
               0x0f  # set GPINTENB to enable pin 0-3 interrupt
               ]

	
	def __init__(self):
		"Intialize port A and then B"
#		global bus
		self.iobus = smbus.SMBus(1)
	        logging.info(self.initialize('A'))
	        logging.info(self.initialize('B'))
	
	def initialize(self, port):
		"Initialize the IO Chip. Port A is output Port B is Keypad"
		try:
			if port =='A':
				self.writedata(self.port_a_dir, 0x00)
        	        	return [1,'Port A initialized']
	        	elif port == 'B':
        	        	for reg, val in zip(self.port_b_regs, self.port_b_vals):
                	        	self.writedata(reg,val)
	                	return [1,'Port B initialized']
        		else:
                		return [-1,'Undefined port']
		except IOError as e:
                	logging.error("I/O error ".format(e.errno, e.strerror))
			raise
		except:
                	logging.error("Error initialzing IO chip")
			raise

	def writedata(self, register, val):
        	self.iobus.write_byte_data(self.address, register, val)
		
	def getbus(self):
		return self.iobus
