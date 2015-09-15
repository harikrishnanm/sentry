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

import io23017 as iochip

bus = smbus.SMBus(1) # For revision 1 Raspberry Pi, change to bus = smbus.SMBus$
address = 0x20 # I2C address of MCP23017
port = 0x12 # GPIOA
default_text = "KRISHNANS"
delay_dur = .001 #s
char_mode_bit ='3'
cmd_mode_bit = '2'
clr_cmd = 0x01
home_cmd ='2'

displaydefault =1

init_vals = [0x32, 0x32, 0x32, #Intialization
	0x22, # Enter 4 bit mode 
	0x22, 0x82, # default was 28 2nd byte 
	0x02, 0x82, # default was 08 
	0x02, 0x12, # default was 01 Clear display
	0x02, 0x62, # default as 06
	0x02, 0xc2 # Bits 11CB
	]
en_port_mask = 0xf0

def initialize():
	"Initialize the LCD."
	iochip.initialize('A') # just in case its not initialzed. 
	splitmask = False # set this for initialization
	for val in init_vals:
       		writelcdcmd(val, splitmask)
	print "initalized"

def clear():

	writelcddata(0x02)
	writelcddata(0x00)
	writelcddata(0x12)
	writelcddata(0x10)
        delay(.002)

def setline():

	writelcddata(0xc2)
        writelcddata(0x00)
	writelcddata(0x02)
        writelcddata(0x00)
	delay(.002)

def curshiftleft():
	writelcddata(0x12)
        writelcddata(0x10)
        writelcddata(0x02)
        writelcddata(0x00)
        delay(.002)

def curshiftright():
        writelcddata(0x12)
        writelcddata(0x10)
        writelcddata(0x42)
        writelcddata(0x40)
        delay(.002)

def writelcdcmd(val, splitmask):
	if splitmask == True:
		# split into two
		x, y = splitbyte(val, cmd_mode_bit)
		print val
		print x,y
		# now write the two bytes
		writelcddata(x)
		writelcddata(y)
	else:	
		print val
		writelcddata(val)
	
def writelcddata(val):
	bus.write_byte_data(address, port, val)
	# and Toggle
	bus.write_byte_data(address,port,en_port_mask)
#        bus.write_byte_data(address,port,val) # this might not be needed.
       	delay()

def writelcdchar(chrasc):
	#Split the bits
	hval, lval = splitbyte(chrasc, char_mode_bit)
#	print hval,lval
	writelcddata(hval)
	writelcddata(lval)
        		        

def splitbyte(bytein, mode_bits):
	h, l = divmod(ord(bytein),16)
        # Add the char mode bits
        h1 = hex(h) + mode_bits
        l1 = hex(l) + mode_bits
        hval = int(hex(int(h1,16)),16)
        lval = int(hex(int(l1,16)),16)
	return hval, lval

def delay(duration=delay_dur):
#	print duration
	time.sleep(duration)

def splitstring(msg):
	x = len(msg)
	words = msg.rsplit()
	print words

def nodefault(val):
	global displaydefault
	displaydefault = val
	print "Display"+str(displaydefault)

def defthread():
        print "active threads:" + str(threading.activeCount())
	while (True and displaydefault == 1):
                clear()
                str_def = default_text.center(16,' ')
                for i in range(0, len(str_def)):
                        writelcdchar(str_def[i])
                localtime = datetime.datetime.now().strftime("%I:%M%p %d %b")
                setline()
                str_def = localtime.center(16,' ')
                for j in range(0,len(str_def)):
                        char1 = str_def[j]
                        writelcdchar(char1)
		delay(60)

def setdefault():
	thread.start_new_thread(defthread, ())

def setmessage(val):
	clear()
	str_def = val.ljust(16,' ')
        for i in range(0, len(str_def)):
        	writelcdchar(str_def[i])


def writemaskedchar(val):
	# display char for some timm
	writelcdchar(val[0]) # just in case the length is > 1 only display first char
	delay(.2)
	# move cursor left
	curshiftleft()
	writelcdchar('*')
#	curshiftright()

def main():
	initialize()
#	setline()
	setdefault()

if __name__ == '__main__':
	main()
	
def __init__(self):
	main()
