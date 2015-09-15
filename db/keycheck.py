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

import MySQLdb as mdb
import sys
import sqlite3 as lite

from memcache import memcache

#+------------+--------------+------+-----+---------+----------------+
#| Field      | Type         | Null | Key | Default | Extra          |
#+------------+--------------+------+-----+---------+----------------+
#| user_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
#| username   | varchar(255) | NO   |     | NULL    |                |
#| email      | varchar(255) | YES  |     | NULL    |                |
#| name       | varchar(255) | YES  |     | NULL    |                |
#| phone      | varchar(255) | YES  |     | NULL    |                |
#| passkey    | varchar(8)   | YES  | UNI | NULL    |                |
#| password   | varchar(255) | YES  |     | NULL    |                |
#| valid_from | datetime     | YES  |     | NULL    |                |
#| valid_to   | datetime     | YES  |     | NULL    |                |
#+------------+--------------+------+-----+---------+----------------+

class keycheck:
	def __init__(self):
		pass

	def getdb(self):
        	try:
                	#con = mdb.connect('localhost', 'root', 'root123', 'sentry');
                	con = lite.connect('/var/tmp/sentry.db')
			#cur = con.cursor()
                	return con
                	#cur.execute("SELECT passkey, name, valid_from, valid_to from u$
                	#res= cur.fetchone()
                	#print res[0]
        	except mdb.Error, e:
                	print "Esddsrror %d: %s" % (e.args[0],e.args[1])
                #finally:
                #	if con:
                #        	con.close()

	def checkKey(self, key):
		
		sql = "select * from user where passkey = \'"
		sql += key
		sql += "\'"
		#print sql
		# check this sql in the memcache
#		ns=Pyro4.naming.locateNS()
#                cache = Pyro4.Proxy("PYRONAME:sentry.cache")
#		if sql in cache.keys():
#			logging.info("Cache HIT")
		
		
		db = self.getdb()
		cur = db.cursor()
		cur.execute(sql)
		res = cur.fetchone()
		cur.close()
		#print res
		del cur
		db.close()
		if res != None:
			return {'name' : res[3], 'valid_from' : res[7], 'valid_to' : res[8]}
		else:
			return None
