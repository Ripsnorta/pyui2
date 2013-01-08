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


class GridLayoutManager(LayoutManager):
    """Grid layout manager
    resizes children in to a grid
    """
    def __init__(self, columns, rows, padding = 3):
        LayoutManager.__init__(self)
        self.padding = padding
        self.columns = columns
        self.rows = rows
        self.posX = 0
        self.posY = 0
        self.full = 0
        
    def begin(self, parent):
        self.posX = parent.posX
        self.posY = parent.posY
        self.colX = 0
        self.rowY = 0
        self.full = 0
        self.columnWidth = self.panel.width / self.columns
        self.rowHeight = self.panel.height / self.rows

    def placeChild(self, child, option):
        if self.full:
            print "grid full!"
            return 
        # NOTE: changing posX/posY directly as an optimization. the correct
        # rect will be calculated below in resize()
        child.posX = self.posX + (self.colX * self.columnWidth) + self.padding
        child.posY = self.posY + (self.rowY * self.rowHeight) + self.padding

        child.resize( self.columnWidth - (self.padding * 2), self.rowHeight - (self.padding * 2) )
        #print child, self.posX, self.posY, self.width, self.height
        self.colX = self.colX + 1
        if self.colX == self.columns:
            self.colX = 0
            self.rowY = self.rowY + 1
            if self.rowY == self.rows:
                self.full = 1
