# pyui2
# Copyright (C) 2005 John Judd
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import string
import pyui2

def getImagePath(filename):
    """getImagePath takes a filename and generates a full path based on the
    location of the images folder in the PyUI2 library.
    """
    pathSep = os.sep
    #print "Separator =", pathSep
    path = pyui2.__path__[0]
    filename = path + pathSep + "images" + pathSep + filename
    return filename

