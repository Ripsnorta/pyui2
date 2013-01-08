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


class TableLayoutManager(LayoutManager):
    """Has a table grid. children can be placed into the grid and take up
    rectangular sections of multiple cells.
    """
    def __init__(self, w, h, padding = 2):
        self.width = w
        self.height = h
        self.padding = padding

    def begin(self, parent):
        self.posX = parent.posX
        self.posY = parent.posY
        self.grid = []        
        self.cellWidth = self.panel.width / self.width
        self.cellHeight = self.panel.height / self.height
        # fill grid with empty cells
        for i in range(0,self.width*self.height):
            self.grid.append(None)
        
        
    def placeChild(self, child, option):
        """placing children in the grid takes an x,y position and a width and height
        in cells that the child takes up. If a cell is occupied a child cannot be
        placed there.
        """
        if len(option) != 4:
            raise ("Child option <%s> wrong for <%s>" % (repr(option), child) )
        
        (x, y, w, h) = option
        if x < 0 or y < 0 or x + w > self.width or y + h > self.height:
            print "error - outside of range of tableLayout."
            return
        # check for empty space
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                offset = xx + yy * self.width
                if self.grid[offset]:
                    print "error - Cannot place at %d,%d occupied by %s" % (xx,yy,self.grid[offset])
                    return
        # populate cells
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                offset = xx + yy * self.width
                self.grid[offset] = child

        # place the child
        child.moveto(self.posX + (x * self.cellWidth) + self.padding, self.posY + (y * self.cellHeight) + self.padding)
        child.resize(w * self.cellWidth - self.padding, h * self.cellHeight - self.padding)
