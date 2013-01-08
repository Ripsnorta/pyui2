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

class AbsoluteLayoutManager(LayoutManager):
    """
    absolute layout manager
    uses direct co-ordinates in a virtual space specified when created
    option must be specified as a (x,y) tuple when adding children
    """
    def __init__(self, w = 100, h = 100):
        self.width = w
        self.height = h

    def setPanel(self, panel):
        self.panel = panel
        
    def begin(self, parent):
        self.posX = parent.posX
        self.posY = parent.posY

    def end(self):
        pass
    
    def placeChild(self, child, option):
        child.moveto(self.panel.width * option[0] / self.width , self.panel.height * option[1] / self.height)

    def canResize(self):
        return true
