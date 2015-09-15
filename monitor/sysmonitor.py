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
import commands, sys
import logging
from gcmclient import gcmhelper

address = 0x27 # I2C address of MCP23017
port = 0x13 # GPIOB
intcap = 0x11 # address of intcapB

sysmon_msgs=['ETH','IP','WLAN','WLAN QUAL','WLAN LEVEL', 'WLAN NOISE', 'IP',
	     'FREE MEM', 'CORE ', 'SDRAM_C ',
	     'SDRAM_I ', 'SDRAM_P ',
	     'CPU TEMP', 'UPTIME']

class sysmonitor(threading.Thread):

	
	def __init__(self, iobusb, dis, lock):
        	logging.info("Initializing System Monitor")
		threading.Thread.__init__(self) # super ini
	        self.bus = iobusb
		self.dis = dis
		self.lock = lock
		self.flag = True

	def run(self):
	        self.checksystem()
	
	def setactive(self, state):
		self.flag = state
		#print "set flag to " + state

	def checksystem(self):
		#flag = True # used to update if needed
		isok = True
		while (self.flag):
			#print self.flag
			sysfile = open( "/sys/class/net/eth0/carrier" )
			eth0link = sysfile.read().replace( '\n', '' )
			sysfile.close()
			if eth0link == '0':
				eth0link = 'DOWN'
			elif eth0link == '1':
				eth0link = 'UP'

			sysfile = open( "/sys/class/net/wlan0/carrier" )
			wlan0link = sysfile.read().replace( '\n', '' )
			sysfile.close()
			wlan_q = 'NA'
			wlan_s = 'NA'
			wlan_n = 'NA'
			if wlan0link == '0':
				wlan0link = 'DOWN'
				if eth0link == 'DOWN':
					# both interfaces down try restart
					logging.warn("Both network interfaces down. Trying to restart")
					#commands.getoutput('/etc/init.d/network restart')
					isok = False
			elif wlan0link == '1':
				wlan0link = 'UP'
				wlan_q =  commands.getoutput('iwconfig wlan0 | grep Link | cut -f2 -d= | cut -f1 -d/')+'%'
				wlan_s =  commands.getoutput('iwconfig wlan0 | grep Link | cut -f3 -d= | cut -f1 -d/')+'%'
				wlan_n =  commands.getoutput('iwconfig wlan0 | grep Link | cut -f4 -d= | cut -f1 -d/')+'%'
			
			#if wlan_q == '':
		#		wlan_q = 'NA'
		#	if wlan_s == '':
                 #               wlan_s = 'NA'
		#	if wlan_n == '':
                 #       	wlan_n = 'NA'

			memory = commands.getoutput( 'free -o | grep "Mem:" | cut -d: -f2' ).lstrip().split()
			freemem = str((1-round(float(memory[1])/float(memory[0]),4))*100)+'%'
			
			volt_core = commands.getoutput( '/opt/vc/bin/vcgencmd measure_volts core | cut -d= -f2' )
			volt_sdram_c = commands.getoutput( '/opt/vc/bin/vcgencmd measure_volts sdram_c | cut -d= -f2' )
			volt_sdram_i = commands.getoutput( '/opt/vc/bin/vcgencmd measure_volts sdram_i | cut -d= -f2' )
			volt_sdram_p = commands.getoutput( '/opt/vc/bin/vcgencmd measure_volts sdram_p | cut -d= -f2' )
			tempSrc_cpu = open( "/sys/class/thermal/thermal_zone0/temp" )
			tripSrc_cpu = open( "/sys/class/thermal/thermal_zone0/trip_point_0_temp" )
			temp_cpu = tempSrc_cpu.read()
			trip_cpu = tripSrc_cpu.read()
			tempSrc_cpu.close()
			tripSrc_cpu.close()
			temp_cpu_c = float( temp_cpu ) / 1000
			#temp_cpu_f = ( 1.8 * temp_cpu_c ) + 32
			trip_cpu_c = float( trip_cpu ) / 1000
			# trip_cpu_f = ( 1.8 * trip_cpu_c ) + 32
			# now we need to write all this into the first line of the display
			procfile = open( "/proc/uptime" )
			contents = procfile.read().split()
			procfile.close()
			unixtime = float( contents[0] )
			minute = 60
			hour = minute * 60
			day = hour * 24
			days = int( unixtime / day )
			hours = int( ( unixtime % day ) / hour )
			minutes = int( ( unixtime % hour ) / minute )
			seconds = int( unixtime % minute )
			uptime = ''
			if days > 0:
				uptime += str( days ) + 'D' # + ( days == 1 and 'Day' or 'Days' ) + ' '
			if len ( uptime ) > 0 or hours > 0:
				uptime += str( hours ) + 'H' # + ( hours == 1 and 'Hour' or 'Hours' ) + ' '
			if len ( uptime ) > 0 or minutes > 0:
				uptime += str( minutes ) + 'M' # + ( minutes == 1 and 'Minute' or 'Minutes' ) + ' '
			uptime += str( seconds ) + 'S' # + ( seconds == 1 and 'Second' or 'Seconds' )

#			ip='NA' # for now
			
			et = commands.getoutput('ip addr show eth0 | grep inet').split()
			
			if len(et) < 1 :
				ethip = 'NA'
			else:
				ethip = et[1]
			
			wl = commands.getoutput('ip addr show wlan0 | grep inet').split()
			if len(wl) < 1 :
                                wlanip = 'NA'
                        else:
                                wlanip1 = wl[1]
				wlanip2 = wlanip1.split('/')
				wlanip = wlanip2[0]

			sysmon_vals=[eth0link, ethip, wlan0link, wlan_q, wlan_s, wlan_n, wlanip, freemem, volt_core, volt_sdram_c, volt_sdram_i, volt_sdram_p, temp_cpu_c, uptime]
			
			for index, msg in enumerate(sysmon_msgs):
				if self.flag:
					#print self.flag
					message = msg+ ':' + str(sysmon_vals[index])
					self.lock.acquire()
					self.dis.setsystemmsg(message)
					self.lock.release()
					time.sleep(2)
			#time.sleep()
			self.lock.acquire()
			self.dis.setsystemmsg("    CHECKED     ")
			self.lock.release()
			time.sleep(2)
