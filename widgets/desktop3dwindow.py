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

from pyui2.desktop import getDesktop, getTheme
from pyui2.window import Window
from pyui2.layouts import Much


class Desktop3DWindow(Window):
    """Special type of Window that is the "background" 3D viewport.
    """
    def __init__(self):
        self._panel = Panel()
        Base.__init__(self)

        # this is identical to Window.__init__
        self.topMost = 0
        self._panel.moveto(0,0)
        Base.addChild(self, self._panel)
        self._panel.setWindow(self)
        getTheme().setArrowCursor()
        self.drawCommands = []
        self.drawLastCallbacks = []
        
        # this is different.. use the desktop
        self.moveto(0, 0)
        self.resize(getDesktop().width, getDesktop().height)
        getDesktop().windows.insert(0,self)

    def destroy(self):
        """dont destroy the background window!
        """
        self._panel = None
        self.handle = 0
        Base.destroy(self)
