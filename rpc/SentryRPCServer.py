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

import rpyc
import threading

from rpyc.utils.server import ThreadedServer

class SentryRPCServer(rpyc.Service, threading.Thread):
	
	def __init__(self):
                print 'Initializing RPC Registry Server'
                threading.Thread.__init__(self) # super ini
		server = ThreadedServer(SentryRPCServer, port=12346)
		server.start()

        def run(self):
                pass

	def on_connect(self):
        	# code that runs when a connection is created
        	# (to init the serivce, if needed)
        	pass

	def on_disconnect(self):
        	# code that runs when the connection has already closed
        	# (to finalize the service, if needed)
        	pass

	def exposed_get_answer(self): # this is an exposed method
        	return 42

	def get_question(self):  # while this method is not exposed
        	return "what is the airspeed velocity of an unladen swallow?"
