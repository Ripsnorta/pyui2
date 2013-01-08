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




#Much is used in computing layouts. It specifies that a widget should be as big as possible.
class __much:
    def __str__(self):
        return "Much"
    __repr__ = __str__
    def __gt__(self, other):
        if other is Much: return 0
        else: return 1
    def __lt__(self, other):
        return 0
    def __ge__(self, other):
        return 1
    def __le__(self, other):
        if other is Much: return 1
        else: return 0
Much = __much()
del __much


class LayoutManager:
    """base class for all layout managers
    """

    # common item alignment flags
    ALIGN_MASK = 0xf000

    XALIGN_MASK = 0x3000
    XCENTER = 0x0000
    XLEFT = 0x1000
    XRIGHT = 0x2000
    XFILL = 0x3000

    YALIGN_MASK = 0xc000
    YCENTER = 0x000
    YTOP = 0x4000
    YBOTTOM = 0x8000
    YFILL = 0xc000

    def __init__(self):
        pass

    def setPanel(self, panel):
        self.panel = panel
        
    def begin(self, parent):
        pass

    def end(self):
        pass
    
    def scanChild(self, child, option):
        pass

    def placeChild(self, child, option):
        pass

    def canResize(self):
        pass

    def destroy(self):
        self.panel = None
