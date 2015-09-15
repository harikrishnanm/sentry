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
class lcdcon:
	
	def initialize(self):
		"Initialize the LCD."
		iochip.initialize('A') # just in case its not initialzed.
	        splitmask = False # set this for initialization
        	for val in init_vals:
                	writelcdcmd(val, splitmask)
	        print "initalized"
