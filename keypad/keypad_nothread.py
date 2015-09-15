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

#passwd = ''
address = 0x20 # I2C address of MCP23017
port = 0x13 # GPIOB
intcap = 0x11 # address of intcapB
keycodes = [0x67, 0xa7, 0xc7, # row 1
            0x6b, 0xab, 0xcb, # row 2
       	    0x6d, 0xad, 0xcd, # row 3
            0x6e, 0xae, 0xce] # row 4

keys = ['1','2', '3', # row 1
	'4','5', '6', # row 2
	'7','8', '9', # row 3
	'x','0', 'y'] # row 4
		
vals = [0x60, 0xa0, 0xc0] # Key scan vals
	
def scankey(bus, dis, timeupdatethread):
	i=0
	passwd = ''
	#print 'passwd ' + passwd
	# do something to ignore the initial value
	while (True):
	        bus.write_byte_data(address, port, vals[i]) # set a pin low
		# wait for a while
		time.sleep(.01)
	        # Read value of interrupt from the ioport. intB is wired to pin 4
		p1 = bus.read_byte_data(address, port)
                intr = p1 & 0x10
	        # check if interrupt is high
		# If high it means some key has been pressed
               	if (intr):
			#print 'interrupt is hig'
                       	var = bus.read_byte_data(address,intcap) & 0b11101111 # read the intcap data
			# print var
                        time.sleep(.01)
       	                # need to check if the key is being held down
               	        # to do that check if the interrupt has been cleared
                       	# read the bits from the port also and block till the values do not match.
                        capval = var & 0x0f
       	                portval = capval
               	        while (portval == capval):
                       	        # keep reading the port till the value changes. i.e the key is released.
                               	# note that this loop will block the outer loop. So the input (b5-7) will not change
                                portval = bus.read_byte_data(address, port) & 0x0f
       				time.sleep(.01)
				# get the code from arrays
			key = keys[keycodes.index(var)]                
			#print 'Incap value='+ key # the moment it changes
			timeupdatethread.displayFlag = 0 # stop the time update thread
			#check for password buffer if first char then do all this
			if len(passwd) == 0:
				dis.clear()
				dis.setmessage("Enter Key...")			
				dis.setline()
			#	print "set"
			elif key == 'y' and passwd != '':
			#	print "y pressed"
				timeupdatethread.displayFlag = 1
				dis.setdefault()
				# send the password elsewhere
				return passwd
			passwd += key
			dis.writemaskedchar(key)
								
		if(i == 2):
        		i = 0
                else:
                     	i += 1
