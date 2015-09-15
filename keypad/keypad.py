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
import logging
import datetime
from db import keycheck
from gcmclient import gcmhelper

class keypad(threading.Thread):
	passwd = ''
	def __init__(self,iocb, busa, busb, dis, consoledis, timeupdatethread, monitorthread, lock):
		threading.Thread.__init__(self)		
		#logging.basicConfig(filename='/var/log/sentry.log',level=logging.DEBUG)
		self.iocb = iocb
		self.bus = busa
		self.busb = busb
		self.dis = dis
		self.timeupdatethread = timeupdatethread
		self.consoledis = consoledis
		self.monitorthread = monitorthread
		self.lock = lock
		self.address = 0x20 # I2C address of MCP23017
		self.port = 0x13 # GPIOB
		self.intcap = 0x11 # address of intcapB
		self.keycodes = [0x67, 0xa7, 0xc7, # row 1
            		    0x6b, 0xab, 0xcb, # row 2
            	    	    0x6d, 0xad, 0xcd, # row 3
		            0x6e, 0xae, 0xce] # row 4

		self.keys = ['1','2', '3', # row 1
        		'4','5', '6', # row 2
        		'7','8', '9', # row 3
        		'x','0', 'y'] # row 4

		self.vals = [0x60, 0xa0, 0xc0] # Key scan vals
		self.keypadtimeout = 5
	
	def run(self):
		while(True):
			keyval = self.scankey()
			#logging.info("Key entered "+keyval)
			#check for entered keyval in mysql
			kc = keycheck()
			result = kc.checkKey(keyval)
			self.timeupdatethread.displayFlag = 0
			if result == None:
				self.lock.acquire()
				self.dis.setmessage("  INVALID  KEY  ")
				self.dis.setmessage2("PLEASE TRY AGAIN")
				self.dis.setline()
				self.lock.release()
				delay = 2
			else:	
				now = datetime.datetime.now()
				if result['valid_from'] < now and result['valid_to'] > now:
					self.dis.setmessage("     WELCOME    ")
					self.dis.setmessage2(result['name'].upper())
					self.lock.acquire()
					self.monitorthread.setactive(False)
					self.lock.release()
					self.consoledis.setsensormsg(" DOOR  UNLOCKED ")
					self.iocb.unlock()
					#gcm message here
					ltime = datetime.datetime.now().strftime("%a, %d %b %H:%M")
					data = {'MSG': 'Unlocked from keypad', 'USER': result['name'], 'TIME': ltime}
					gcmhelp = gcmhelper()
					gcmhelp.sendgcmsg(data, keyval)
					delay = 0
				else:
					self.lock.acquire()
					self.dis.setmessage("**KEY  EXPIRED**")
					delay = 2
					self.dis.setmessage2(result['name'].upper())
					self.lock.release()
			time.sleep(delay)
			self.timeupdatethread.displayFlag = 1
			self.monitorthread.setactive(True)
			self.lock.acquire()
			self.dis.clear()
			self.dis.setdefault()
			self.lock.release()
			
	
	
	def scankey(self):
		i=0
	        passwd = ''
        	address = self.address
		port = self.port
		vals = self.vals
		keys = self.keys
		intcap = self.intcap
		keycodes = self.keycodes
		dis = self.dis
		timeupdatethread = self.timeupdatethread
		bus = self.bus
		lastpresstime = ''

        	# do something to ignore the initial value
		key=''
        	while (True):
			#check if there is an entered value and if time has expired
			#if lastpress !='' and datetime.datetime.now()-lastpress > 5
				#clear the password and display
			#	passwd=''
                	try:
				bus.write_byte_data(address, port, vals[i]) # set a pin low
				# wait for a while
                		time.sleep(.08)
                		# Read value of interrupt from the ioport. intB is wired to pin 4
                		p1 = bus.read_byte_data(address, port)
                	except IOError as e:
                                logging.error("I/O error ".format(e.errno, e.strerror))
                        except:
                                logging.error("Key scan error")
			intr = p1 & 0x10
                	# check if interrupt is high
                	# If high it means some key has been pressed
                	if (intr):
                        	#print 'interrupt is hig'
                        	try:
					var = bus.read_byte_data(address,intcap) & 0b11101111 # read the intcap data
				except IOError as e:
                                	logging.error("I/O error ".format(e.errno, e.strerror))
                        	except:
                                	logging.error("Key scan error")
                        	# print var
                        	time.sleep(.06)
                        	# need to check if the key is being held down
				# to do that check if the interrupt has been cleared
                        	# read the bits from the port also and block till the values do not match.
                        	capval = var & 0x0f
                        	portval = capval
                        	while (portval == capval):
                                	# keep reading the port till the value changes. i.e the key is released.
                                	# note that this loop will block the outer loop. So the input (b5-7) will not change
                                	try:
						portval = bus.read_byte_data(address, port) & 0x0f
					except IOError as e:
                                        	logging.error("I/O error ".format(e.errno, e.strerror))
                                	except:
                                        	logging.error("Key scan error")
                                	
				time.sleep(.01)
                                # get the code from arrays try catch to handle any transient data
                        	try:
					key = keys[keycodes.index(var)]
				except:
					key=''

                        	#print 'Incap value='+ key # the moment it changes
                        	timeupdatethread.displayFlag = 0 # stop the time update thread

                        	# start stopwatch here
				lastpresstime = time.time()
				#if key == 'x':
				#	passwd =''
				#else:
				#	passwd += key
	                                #dis.writemaskedchar(key)
				#check for password buffer if first char then do all this
                        	if len(passwd) == 0:
					self.lock.acquire()
                                	dis.clear()
                                	dis.setmessage("Enter Key...")
                                	dis.setline()
					self.lock.release()

                        	#       print "set"
				#	elif key == 'x' and passwd != '':
				#	passwd = ''
				#	#logging.info("Clearing password "+ passwd)
				#	timeupdatethread.displayFlay = 1
				#	dis.setdefault()
                        	elif key == 'y' and passwd != '':
				       	#print "y pressed"
                                	# timeupdatethread.displayFlag = 1
                                	# dis.setdefault()
                                	# send the password elsewhere
					return passwd
				#elif key == 'y' and passwd == '':
				#	timeupdatethread.displayFlag = 1
				
				# if no key has been pressed reset display by setting the key to x

                        	passwd += key
				self.lock.acquire()
                        	dis.writemaskedchar(key)
				self.lock.release()

				if key == 'x' and passwd != '':
					timeupdatethread.displayFlag = 1
					self.lock.acquire()
					dis.setdefault()
					self.lock.release()
					passwd = ''
			# check if last pressed time has exceeded the preset time.
                	if lastpresstime != '' and time.time()- lastpresstime > self.keypadtimeout:
				timeupdatethread.displayFlag = 1
                                self.lock.acquire()
                                dis.setdefault()
                                self.lock.release()
                                passwd = ''
				lastpresstime = ''

			if(i == 2):
                        	i = 0
                	else:
                        	i += 1

