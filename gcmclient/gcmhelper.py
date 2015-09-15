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

from gcmclient import *
from db import dbutil
import json

class gcmhelper:
	#gcm = GCM('AIzaSyBfPDU7I2GltOSwp2UWLhEkR0TJO-QuPd4') #API key
	#dbut = dbutil()
	# get ids
	#devids = dbut.getdevids()
	#print devids
	def sendgcmsg(self, msg, key):
		#print devids 
		#TODO use key to exclude if key is -1 send to all. 
		#global devids
		gcm = GCM('AIzaSyBfPDU7I2GltOSwp2UWLhEkR0TJO-QuPd4') #API key
	        dbut = dbutil()
		#devenum = dbut.getdevids()
		devdata = dbut.getdevids()
		#de_data = kursor.fetchall()
    		devlist = []
    		for index in range(len(devdata)):
       	 		devlist.append(devdata[index][0])
				
		#print msg
		#print devlist
		multicast = JSONMessage(devlist, msg, collapse_key='com.krishnans.sentry', dry_run=False)
		try:
	 		res_multicast = gcm.send(multicast)

			#for reg_id, msg_id in res.success.items():
	            	#print "Sent GCM Messgae"

		except GCMAuthenticationError:
   			# stop and fix your settings
    			print "Your Google API key is rejected"
		except ValueError, e:
    			# probably your extra options, such as time_to_live,
    			# are invalid. Read error message for more info.
    			print "Invalid message/option or invalid GCM response"
    			print e.args[0]
		except Exception, e :
    			# your network is down or maybe proxy settings
    			# are broken. when problem is resolved, you can
    			# retry the whole message.
    			print "Something wrong with requests library"
			print e.args[0]
# Pass 'proxies' keyword argument, as described in 'requests' library if you
# use proxies. Check other options too.
#gcm = GCM('AIzaSyBfPDU7I2GltOSwp2UWLhEkR0TJO-QuPd4')

# Construct (key => scalar) payload. do not use nested structures.
#data = {'MSG': 'UNLOCKED'}
#regid = ' APA91bGmZY6n5VdWb3fYdaV98uEHbA0oY2ygjOtzINqrvMqACQ9HICUQ6VQO4hIXdvC0AwGvf-8-vTkc2NAeTp3-Rn327AqtFq7Z3-87L1qQbpuW4AuMzN6Nk4UCUGxrxaMW1mNpAAWMSmZSS1to7_u-dTnWHjzXIA'

# Unicast or multicast message, read GCM manual about extra options.
# It is probably a good idea to always use JSONMessage, even if you send
# a notification to just 1 registration ID.
#unicast = PlainTextMessage(regid, data, dry_run=False)
#multicast = JSONMessage([regid], data, collapse_key='my.key', dry_run=False)

#try:
    # attempt send
#    res_unicast = gcm.send(unicast)
#    res_multicast = gcm.send(multicast)

#    for res in [res_unicast, res_multicast]:
        # nothing to do on success
#        for reg_id, msg_id in res.success.items():
#            print "Successfully sent %s as %s" % (reg_id, msg_id)

        # update your registration ID's
#        for reg_id, new_reg_id in res.canonical.items():
#            print "Replacing %s with %s in database" % (reg_id, new_reg_id)

        # probably app was uninstalled
#        for reg_id in res.not_registered:
#            print "Removing %s from database" % reg_id

        # unrecoverably failed, these ID's will not be retried
        # consult GCM manual for all error codes
#        for reg_id, err_code in res.failed.items():
#            print "Removing %s because %s" % (reg_id, err_code)

        # if some registration ID's have recoverably failed
#        if res.needs_retry():
            # construct new message with only failed regids
#            retry_msg = res.retry()
            # you have to wait before attemting again. delay()
            # will tell you how long to wait depending on your
            # current retry counter, starting from 0.
#            print "Wait or schedule task after %s seconds" % res.delay(retry)
            # retry += 1 and send retry_msg again

#except GCMAuthenticationError:
    # stop and fix your settings
#    print "Your Google API key is rejected"
#except ValueError, e:
    # probably your extra options, such as time_to_live,
    # are invalid. Read error message for more info.
#    print "Invalid message/option or invalid GCM response"
#    print e.args[0]
#except Exception:
    # your network is down or maybe proxy settings
    # are broken. when problem is resolved, you can
    # retry the whole message.
#    print "Something wrong with requests library"
