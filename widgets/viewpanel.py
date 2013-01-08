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
from pyui2.panel import Panel
from pyui2.layouts import Much


class ViewPanel(Panel):
    """A rectangle intended as a viewport into a 3D world. The implementation of worlds is very renderer
    specific. The only real constraint placed by pyui2 is that the world lifetime is controlled by
    createWorld/destroyWorld. The handle returned from createWorld should be used to identify it in
    any further operations.
    """
    def __init__(self, world, windowHandle, width, height):
        Panel.__init__(self)
        #self.viewHandle = getRenderer().createView(world)
        self.world = world
        self.windowHandle = windowHandle

        ## attach to the desktop background windowHandle.
        primView = (pyui2.locals.VIEW, 0, 0, width, height, self.viewHandle)

        # add the world view to the desktop window 'container'
        #getRenderer().describeWindow(windowHandle, [primView,])

    def destroy(self):
        #print "Destroying view:", self.viewHandle
        self.windowHandle = None
        #getRenderer().destroyView(self.viewHandle)
        Panel.destroy(self)

#    def draw(self, renderer):
#        pass
        #renderer.drawView(self.windowRect, self.viewHandle)

    def setEffect(self, effectName):
        pass
        #getRenderer().setWindowEffect(self.windowHandle, effectName)

