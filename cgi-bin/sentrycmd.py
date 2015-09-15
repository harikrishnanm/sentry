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

import sys
import json
import Pyro4

def getcommand():
        global jsondata
        return jsondata["CMD"]

def lock():
        global jsondata
        checkauthp()
	#Pyro4.config.HMAC_KEY = '12345'
	id = jsondata["ID"]
        # call the script to lock here, pass id as param
	#ns=Pyro4.naming.locateNS()
        #sproxy = Pyro4.Proxy("PYRONAME:sentry.proxy")
	sproxy.lock()
        # for now assume result is success
        sys.stdout.write("Sentry: Locked %s" % id)
        response_success = [ {'RESPONSE':'OK','STATUS':'LOCKED'} ]
        response_success_json = json.dumps(response_success)
        print "Content-type: application/json\r\r\r\n"
        print "%s" % (response_success_json)

def getstate():
	#checkauthp()
	state = sproxy.getstate()
	response_state = [ {'RESPONSE':'OK','STATE':state} ]
	response_state_json = json.dumps(response_state)
	print "Content-type: application/json\r\r\r\n"
        print "%s" % (response_state_json)
	
def unlock():
        global jsondata
	checkauthp()
	id = jsondata["ID"]
        sproxy.unlock()
        sys.stdout.write("Sentry: Unlocked %s" % id)
        response_success = [ {'RESPONSE':'OK','STATUS':'UNLOCKED'} ]
        response_success_json = json.dumps(response_success)
        print "Content-type: application/json\r\r\r\n"
        print "%s" % (response_success_json)

def regid():
	# put id in DB here.
	global jsondata
	regid = jsondata["REGID"]
	sproxy.addregid(regid)
	response_success = [ {'RESPONSE':'OK','STATUS':'REGID_ADDED'} ]
        response_success_json = json.dumps(response_success)
        print "Content-type: application/json\r\r\r\n"
        print "%s" % (response_success_json)

def alert():
        global jsondata
        key = jsondata["KEY"]
        #sproxy.sendnotification(key)


def checkauthp():
        global jsondata
	global imei
	global imsi
	global key

	authorization = sproxy.authdev(imei,imsi,key)
	if authorization == 0:
		response_auth = [ {'RESPONSE':'OK','STATUS':'UNAUTHORIZED'} ]
		response_auth_json = json.dumps(response_auth)
        	print "Content-type: application/json\r\r\r\n"
        	print "%s" % (response_auth_json)
		sys.exit(0)
	if authorization == 2:
		response_auth = [ {'RESPONSE':'OK','STATUS':'AUTH EXPIRED'} ]
                response_auth_json = json.dumps(response_auth)
                print "Content-type: application/json\r\r\r\n"
                print "%s" % (response_auth_json)
                sys.exit(0)

#sys.stdout.write("Sentry: Locked %s" % id)
Pyro4.config.HMAC_KEY = '12345'
Pyro4.config.BROADCAST_ADDRS = "127.0.0.1"
#Pyro4.config.SERIALIZER = 'pickle'
ns=Pyro4.naming.locateNS()
sproxy = Pyro4.Proxy("PYRONAME:sentry.proxy")
data = sys.stdin.read()
sys.stderr.write("data"+str(data))
if data =='':
        print "Content-type: text/html\r\r\r\n"
	print "Do not try tricks"
        sys.exit(0)
#sys.stderr.write(data)
jsondata = json.loads(data)
sys.stderr.write("JSON DATA"+str(jsondata))
try:
	imei = jsondata["IMEI"]
	imsi = jsondata["IMSI"]
	key = jsondata["KEY"]
except KeyError:
	pass #ignore for now
#checkauthp()

#sproxy.checkauth(imei, imsi, key)
#if authrorization == 0:
	

# First check auth
# then get the command and invoke the right script

command = getcommand()

if command == "UNLOCK": # unlock the door
	unlock()
	alert()
elif command == "LOCK": # lock the door
	lock()
elif command == "GETSTATE":
	getstate()
elif command == "LOCKDOWN": # lockdown, activate door closure if not closed
	pass
elif command == "ADDUSER": # add user
	pass
elif command == "DELUSER": # delete user
	pass
elif command == "NOKEY": # disable keypad
	pass
elif command == "REGID":
	regid()
