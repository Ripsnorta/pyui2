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

import pyui2

from pyui2.desktop import getDesktop, getTheme, getPresenter
from pyui2.window import Window
from pyui2.layouts import Much


class TooltipWindow(Window):
    """A window that displays tooltips.
    """
    def __init__(self, x, y, w, h):
        Window.__init__(self, x, y, w, h, 1)#, "tooltip")
        self.setLayout(pyui2.layouts.BorderLayoutManager())
        self.text = ""
        self.setShow(0)
        
    def activate(self, text, rect):
        #print "Enabling", self, rect
        self.text = text
        self.moveto(rect[0], rect[1])
        self.resize(rect[2], rect[3])
        self.setShow(1)

