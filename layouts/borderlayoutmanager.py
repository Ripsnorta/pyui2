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

from layoutmanager import LayoutManager


class BorderLayoutManager(LayoutManager):
    """Border layout manager
    preserves one-dimensional sizes of children
    will not change the size of the parent
    """
    WEST = 1
    EAST = 2
    NORTH = 3
    SOUTH = 4
    CENTER = 5
    
    def __init__(self,padding = 2):
        LayoutManager.__init__(self)
        self.padding = padding
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.center = None

    def begin(self, parent):
        self.posX = parent.posX
        self.posY = parent.posY
        self.middleX0 = 0
        self.middleY0 = 0
        self.middleX1 = self.panel.width
        self.middleY1 = self.panel.height
        
    def scanChild(self, child, option):
        if option == BorderLayoutManager.NORTH:
            self.middleY0 = child.height + self.padding
            self.north = child
        elif option == BorderLayoutManager.SOUTH:
            self.middleY1 = self.panel.height - child.height - self.padding
            self.south = child
        elif option == BorderLayoutManager.EAST:
            self.east = child
            self.middleX1 = self.panel.width - child.width - self.padding
        elif option == BorderLayoutManager.WEST:
            self.middleX0 = child.width + self.padding
            self.west = child
        elif option == BorderLayoutManager.CENTER:
            self.center = child

    def placeChild(self, child, option):
        if self.north:
            self.north.moveto(self.posX, self.posY)
            self.north.resize(self.panel.width, self.north.height)
        if self.south:
            self.south.moveto(self.posX, self.posY + self.middleY1 + self.padding)
            self.south.resize(self.panel.width, self.south.height)
        if self.west:
            self.west.moveto(self.posX, self.posY + self.middleY0)
            self.west.resize(self.west.width, self.middleY1 - self.middleY0)
        if self.east:
            self.east.moveto(self.posX + self.middleX1 + self.padding, self.posY + self.middleY0)
            self.east.resize(self.east.width, self.middleY1 - self.middleY0)
        if self.center:
            self.center.moveto(self.posX + self.middleX0, self.posY + self.middleY0)
            self.center.resize(self.middleX1 - self.middleX0, self.middleY1 - self.middleY0)
        
    def canResize(self):
        return true

    def destroy(self):
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.center = None
        layoutManager.destroy(self)
