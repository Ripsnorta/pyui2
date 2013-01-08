# pyui2
# Copyright (C) 2001-2002 Sean C. Riley
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

"""Some default colors for use in pyui2 applications.
These get packed by the specified renderer at initialization.
"""

black = 0
white = 0
red = 0
green = 0
blue = 0
grey = 0
yellow = 0
orange = 0

def init():
    global black, white, red, green, blue, grey, yellow, orange
    black =   (0,   0,   0, 255)
    white =   (255, 255, 255, 255)
    red =     (255, 0,   0, 255)
    green =   (0,   255, 0, 255)
    blue =    (0,   0,   255, 255)
    grey =    (150, 150, 150, 255)
    yellow =  (255,255,0, 255)
    orange =  (255,128,0, 255)
    
    

