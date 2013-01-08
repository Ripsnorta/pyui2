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


class FlowLayoutManager(LayoutManager):
    """Flow layout manager
    preserves sizes of children - horizontal layout
    """
    NEWLINE = 1
    def __init__(self,padding = 0):
        LayoutManager.__init__(self)
        self.padding = padding
        self.scanX = self.padding
        self.lastY = self.padding
        self.maxY = 0
        
    def begin(self, parent):
        self.posX = parent.posX
        self.posY = parent.posY
        self.scanX = self.padding        
        self.lastY = self.padding
        self.maxY = 0
        self.positions = []             # list of (x_position, row, width) tuples
        self.row_heights = [0]          # tallest item in each row
        
    def scanChild(self, child, option):
        # determine X position, and determine height of current row

        new_row = 0
        width, height = child.getPreferredSize()

        # go to a new line if specified or if this line is out of space
        if option == None:
            option = 0
        if (((option & ~self.ALIGN_MASK) == self.NEWLINE
             and self.scanX > self.padding)
            or (self.scanX > 0
                and self.scanX + width > self.panel.width)):
            #newline
            self.scanX = self.padding
            self.row_heights.append(0)
            new_row = 1

        # preserve data for use during placement
        self.positions.append((self.scanX, new_row, width))
        self.scanX = self.scanX + self.padding + width
        self.row_heights[-1] = max(self.row_heights[-1], height)
        
    def placeChild(self, child, option):
        # determine Y position and move child to its position
        
        # get next child data from head of list
        x_position, new_row, width = self.positions[0]
        del self.positions[0]

        # go to next row if indicated
        if new_row:
            self.lastY = self.row_height + self.padding
            del self.row_heights[0]
        self.row_height = self.row_heights[0]

        # move and size child based on alignment options
        if option == None:
            option = 0
        yalign_option = option & self.YALIGN_MASK
        max_height = child.getMaximumSize()[1]

        if max_height >= self.row_height or yalign_option == self.YFILL:
            child.moveto(self.posX + x_position, self.posY + self.lastY)
            child.resize(width, self.row_height)
        elif yalign_option == self.YCENTER:
            child.resize(width, max_height)
            child.moveto(self.posX + x_position, self.posY + self.lastY + (self.row_height - child.height) // 2)
        elif yalign_option == self.YBOTTOM:
            child.resize(width, max_height)
            child.moveto(self.posX + x_position, self.posY + self.lastY + self.row_height - child.height)
        elif yalign_option == self.YTOP:
            child.resize(width, max_height)
            child.moveto(self.posX + x_position, self.posY + self.lastY)
        

    def canResize(self):
        return false    
