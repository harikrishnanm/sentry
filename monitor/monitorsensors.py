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
import math
import logging
import datetime
from gcmclient import gcmhelper

address = 0x27 # I2C address of MCP23017
port = 0x13 # GPIOB
intcap = 0x11 # address of intcapB

state = "Not Set" # init

class monitorsensors(threading.Thread):
	
	def __init__(self, iocb, iobusb, dis, lock):
        	logging.info("Initializing EM and Exit switch monitors")
		threading.Thread.__init__(self) # super ini
		self.ioc = iocb
	        self.bus = iobusb
		self.dis = dis
		self.lock = lock
		self.activeflag = True

	def run(self):
	        self.checkstate()
	
	def setactive(self, state):
		self.activeflag = state
		self.flag = state

	def getstate(self):
		#logging.info("State queried. Returning "+ self.state )
		return self.state

	def checkstate(self):
		#state
		self.flag = True # used to update if needed
		oldval = 99999 # init
		ptime = 0 # init
		pressedtime=0
		exitpflag = 0 #ini
		while (True):
			#self.dis.setsensormsg("CHECKING SENSORS")
			portval = self.bus.read_byte_data(address, port) & 0xf0 # read only 4-7
			# time.sleep(2)
			# flag = True # used to update if needed
			#logging.debug('Portval ' + str(portval)) 
			#logging.info('looping') 
			# print flag, self.activeflag
			
			if portval != oldval: # if there is a change enter the code 
				oldval = portval
				#sensor = int(math.log(portval,2))+1 # this is crude for now Cannot handle mutiple sensors.
				# get sensors
				# first check for bit 5
				# mesg  = 'SENSORS: ' + str(sensor)
				#print sensor
				#check if exit switch is pressed
				# Normal - 96 Exit Pressed 112
				# Open - 0 Exit Pressed 16
				# Top Disengaged - 64 Exit Pressed 80
				# Bottom Disengaged - 32 Exit Pressed 48
				
				# TODO
				# we are only checking 3 bits where as 4 are being read. The fourth bit is unpredictable and can cause issues. 
				# however we are setting the pullup on so should be ok. Better is to rewrite the code to take care of the 4th bit. 

				if portval == 16 or portval == 112 or portval == 48 or portval == 80:
					mesg = 'EXIT SWITCH'
					self.state = mesg
					self.lock.acquire()
                                        self.dis.initialize()# reinit just in case
					self.dis.setsensormsg(mesg)
                                        self.lock.release()
					# this is where we need to start a counter for long press. 
					# right now it unlocks on press
					# need to change this to un
					# Need to introduce another variable - timepressed and have an if then switch to handle time ranges
					# so need to
					# ptime = datetime.datetime.now()
					# unlock the door first
					#self.ioc.unlock()
					#record the time 
					#self.ioc.open()
					# if portval is 112, do not close

					self.ioc.unlock()
					#
					pressedtime = datetime.datetime.now()
					#send notification here
					ltime = datetime.datetime.now().strftime("%a, %b %H:%M")
                                        data = {'MSG': 'Unlocked - Exit Switch','USER':'', 'TIME': ltime}
                                        gcmhelp = gcmhelper()
                                        gcmhelp.sendgcmsg(data,'-1')# -1 so that its sent to all
					self.flag = True
					#if portval == 112: # the exit switch is pressed
						# do not re-engage the lock
						# 
				elif portval == 0:
					mesg  = 'ALL DISENGAGED'
					self.state = 'DOOR UNLOCKED'
					# send notification
					self.lock.acquire()
					self.dis.initialize()
					self.dis.setsensormsg(mesg)
					self.lock.release()
					self.flag = True
				elif portval == 64:
					mesg = 'TOP DISENGAGED'
					self.state = mesg
					self.lock.acquire()
					self.dis.initialize()
                                        self.dis.setsensormsg(mesg)
                                        self.lock.release()
					self.flag = True
				elif portval == 32: 
					mesg = 'BOT DISENGAGED'
					self.state = 'BOTTOM DISENGAGED'
                                        self.lock.acquire()
                                        self.dis.initialize()
					self.dis.setsensormsg(mesg)
                                        self.lock.release()
					self.flag = True
				elif portval == 96: 
					# dont keep updating display for the heck of it.
					mesg = 'LOCKS ENGAGED:OK'
					self.state = mesg
					if self.flag:
						self.lock.acquire()
						self.dis.initialize()
						self.dis.setsensormsg(mesg)
						self.lock.release()
						self.flag = False
				
				else:
					mesg = 'SYSTEM ERROR:'+ porttval
					self.state = mesg
					self.lock.acquire()
                                        self.dis.setsensormsg(mesg)
                                        self.lock.release()
                                        self.flag = False
				# # this is where we need to find when the switch is released
                                #releasetime = datetime.datetime.now()
                                #difftime = releasetime - pressedtime
                                #if difftime > 5 and difftime < 10:
                                #	logging.info('REBOOT SYSTEM')
                                #elif difftime > 10:
                                #        logging.info('HALT SYSTEM')
			time.sleep(.01)	
