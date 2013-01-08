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

import pyui2

from pyui2.desktop import getDesktop, getPresenter
from pyui2.base import Base
from pyui2.layouts import Much
from pyui2.widgets import Frame

#############################################################################################################
##
#############################################################################################################
class Toolbar(Frame):
    ALIGN_TOP = 1
    ALIGN_LEFT = 2
    ALIGN_BOTTOM = 3
    ALIGN_RIGHT = 4
    
    def __init__(self, alignment=ALIGN_TOP):
        flags = []
        flags.append(pyui2.widgets.Frame.NO_RESIZE)
        flags.append(pyui2.widgets.Frame.NO_CAPTION)
        #flags.append(pyui2.widgets.Frame.TOPMOST)
        
        self.determinePlacement(alignment)
        
        Frame.__init__(self, self.posX, self.posY, self.width, self.height, None, flags)
        
        
    def determinePlacement(self, alignment):
        self.alignment = alignment
        
        (width, height) = getDesktop().getSize()
        if alignment == Toolbar.ALIGN_TOP or alignment == Toolbar.ALIGN_BOTTOM:
            self.width = width
            self.height = 32
        elif alignment == Toolbar.ALIGN_LEFT or alignment == Toolbar.ALIGN_RIGHT:
            self.width = 32
            self.height = height
            
        if alignment == Toolbar.ALIGN_TOP or alignment == Toolbar.ALIGN_LEFT:
            self.posX = 0
            self.posY = 0
        elif alignment == Toolbar.ALIGN_BOTTOM:
            self.posX = 0
            self.posY = height - self.height
        elif alignment == Toolbar.ALIGN_RIGHT:
            self.posX = width - self.width
            self.posY = 0
            
        
        
        
        
        
        
        
        