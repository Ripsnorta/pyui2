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


class AttachedWindow(Window):
    """A Window that is attached to a 3D object.
    NOTE: careful that these may not have co-ordinates updated - dont make these interactive
    NOTE: maybe all windows should have this functionality... then Frames could use it...
    """
    def __init__(self, xoffset, yoffset, width, height, objectHandle, viewHandle, nodeName = None):
        Window.__init__(self, 0, 0, width, height)
        #controllerHandle = getRenderer().attachController(objectHandle, pyui2.locals.CONTROLLER_2DWINDOW, nodeName)
        #getRenderer().setController(controllerHandle, window = self.handle, offset = (xoffset, yoffset), view = viewHandle)
        self.viewHandle = viewHandle
        self.objectHandle = objectHandle
        self.controllerHandle = controllerHandle
        self.nodeName = nodeName
        self.xoffset = xoffset
        self.yoffset = yoffset
        
    def destroy(self):
        #getRenderer().detachController(self.objectHandle, self.controllerHandle)
        self.controllerHandle = None
        Window.destroy(self)

