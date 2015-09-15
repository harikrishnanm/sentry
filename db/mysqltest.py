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


def getdb():
        try:
                con = mdb.connect('localhost', 'root', 'root123', 'sentry');
#                cur = con.cursor()
                return con
                #cur.execute("SELECT passkey, name, valid_from, valid_to from user where passkey = '1975'")
                #res= cur.fetchone()
                #print res[0]
        except mdb.Error, e:
                print "Esddsrror %d: %s" % (e.args[0],e.args[1])
                sys.exit(1)

#        finally:
#                if con:
#                        con.close()

def adduser(username, email, name, phone, passkey, password, valid_from, valid_to):
        sql = "INSERT INTO user (USERNAME, EMAIL, NAME, PHONE, PASSKEY, PASSWORD, VALID_FROM, VALID_TO)"
        sql += " VALUES ('"
        sql += username + "', '"
	sql += email + "', '"
	sql += name + "', '"
	sql += phone + "', '"
	sql += passkey + "', '"
	sql += password + "', '"
	sql += valid_from + "', '"
	sql += valid_to + "')"
	print sql	
	db = getdb()
	cur = db.cursor()
	cur.execute(sql)
	db.commit()
	


def main():
	adduser('lekh1', 'krishnan.lekha@gmail.com', 'Lekha Krishnan', '+91 99805 69428', '1978', '*', '2013-8-29 19:00:00', '9999-12-31 23:59:59')
#	adduser('hari', 'harikrishnanm@gmail.com', 'Harikrishnan M', '+91 99805 31750', '1975', '*', '2013-8-29 19:00:00','9999-12-31 23:59:59')
	
if __name__ == "__main__":
        main()

