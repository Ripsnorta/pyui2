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
from pyui2.base import Base
from pyui2.frame import Frame
from pyui2.layouts import Much


class ViewWindow(Frame):
    """A window that contains a ViewPanel
    """
    def __init__(self, x, y, w, h, world):
        Frame.__init__(self, x, y, w, h, "3d!")
        panel = ViewPanel(world)
        self.replacePanel(panel)
        self.world = world

