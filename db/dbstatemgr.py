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

import pyinotify
import logging
import hashlib
import shutil
import os.path
import threading
import system

from memcache import memcache, memcachemgr 

DB_FILE_SAVED = '/home/pi/sentry/sentry/db/sqlite/sentry_saved.db'
DB_FILE_BOOTSTRAP = '/home/pi/sentry/sentry/db/sqlite/sentry_bootstrap.db'
DB_FILE_ACTIVE = '/var/tmp/sentry.db'

bootstrap = 1
checkflag = False
dbmemcache = None

event_flags = pyinotify.IN_MODIFY | pyinotify.IN_ACCESS
notifier = None

class dbstatemgr(pyinotify.ProcessEvent, threading.Thread):
	def __init__(self, cachemgr):
		global bootstrap, dbmemcache
		self.dbmemcache = cachemgr
		logging.info('Initializing DB State Manager')
		threading.Thread.__init__(self)
		if os.path.exists(DB_FILE_SAVED):
                	logging.info('Saved state found. Restoring as active')
                	shutil.copy(DB_FILE_SAVED, DB_FILE_ACTIVE)
			bootstrap = 0
        	else:
                	logging.info('No saved state. Restoring bootstrap data')
                	shutil.copy(DB_FILE_BOOTSTRAP, DB_FILE_ACTIVE)
			bootstrap =1

		logging.debug('DB State manager initialized')
	#	logging.info('Starting DB event monitor thread')
	#	event_flags = pyinotify.IN_MODIFY | pyinotify.IN_ACCESS
    	#	wm = pyinotify.WatchManager()
    	#	wm.add_watch(DB_FILE_ACTIVE, event_flags, rec=True)

    		# event handler
	#	notifier = pyinotify.ThreadedNotifier(wm, self)
    	#	notifier.run()
    	
	def process_IN_ACCESS(self, event):
        	global checkflag
		logging.debug('Checkflag in access: '+ str(checkflag))
		if checkflag == True:
			logging.debug("ACCESS event: DB file: "+ event.pathname)
			self.handleevent()
    	def process_IN_MODIFY(self, event):
        	global checkflag
		if checkflag:
			logging.debug("MODIFY event: DB file: "+ event.pathname)
    			self.handleevent()
	
	def handleevent(self):
		global bootstrap
		self.endwatch()
		# cmdutil = pycommands()
		logging.info("DB Accessed/Modified. Check hash")
		try:
			activehash = hashlib.md5(open(DB_FILE_ACTIVE).read()).hexdigest()
			logging.debug('Active Hash= '+activehash)
			if bootstrap == 0: # check saved file
				logging.info('Checking saved hash')
				if os.path.exists(DB_FILE_SAVED):
					savedhash = hashlib.md5(open(DB_FILE_SAVED).read()).hexdigest()
					logging.debug('Saved Hash= '+savedhash)
				else:
					logging.error('An error has occured. A file that is needed cannot be found')
			else:
				logging.info('Checking bootstrap hash')
                                boothash = hashlib.md5(open(DB_FILE_BOOTSTRAP).read()).hexdigest()
                              	logging.debug('Bootstrap hash'+ boothash)
                                savedhash = boothash
			
			if activehash != savedhash:
				logging.info('DB state changed saving new state')
				# remount the filesystem rw and then copy the file.
				logging.debug('Remounting filesystem RW')
				os.system("sudo mount -o rw,remount /")
				shutil.copy(DB_FILE_ACTIVE, DB_FILE_SAVED)
				logging.debug('Remounting filesystem RO')
				os.system("sudo sync")
				#os.system("sudo mount -o ro,remount /")
				cmdutil.remountro()
				logging.info('New DB file saved')
				logging.debug('Clearing cache')
				self.dbmemcache.clearcacheimd()
				bootstrap = 0
			else:
				logging.info('DB state unchanged')
		
		except IOError, e:
                        logging.error(e)
		finally:
			self.startwatch()			
	def run(self):
		global checkflag
		checkflag = True
		logging.info('Starting DB event monitor thread')
                self.startwatch()

	def startwatch(self):
		global event_flags, notifier
		logging.info('Starting notifier')
		event_flags = pyinotify.IN_MODIFY | pyinotify.IN_ACCESS
                wm = pyinotify.WatchManager()
                wm.add_watch(DB_FILE_ACTIVE, event_flags, rec=True)
                # event handler
                notifier = pyinotify.Notifier(wm, self)
                notifier.loop()
	
	def endwatch(self):
		global notifier
		logging.info('Stopping notifier')
		notifier.stop()
