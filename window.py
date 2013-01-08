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
from pyui2.base import Base
from pyui2.panel import Panel
from pyui2.desktop import getDesktop, getTheme, getPresenter
from pyui2 import layouts


class Window(Base):
    """window - contains other objects.
    Windows have a main panel (_panel) which can be replaced with a custom panel. this main panel is
    kept the size of the interior of the window.
    """

    def __init__(self, x, y, w, h, topmost = 0):
        self._panel = Panel()
        Base.__init__(self)
        self.topMost = topmost
        # the content panel is added as a child through Base::addChild to avoid recursively adding it to itself
        Base.addChild(self, self._panel)
        self._panel.setWindow(self)
        self._panel.setParent(self)
        self.placeInnerObjects()

        self.drawCommands = []
        # these are drawing callbacks to draw _after_ all the widgets are drawn
        self.drawLastCallbacks = []
        self.moveto(x, y)
        self.resize(w, h)
        getDesktop().addWindow(self)

        # Create the graphics context that will be used to display this window
        self.graphicsContext = getPresenter().getDeviceContext().createGraphicsContext((w, h))


    def getGraphicsContext(self):
        return self.graphicsContext

    def beginDraw(self):
        self.graphicsContext.beginDraw(self.posX, self.posY)

    def endDraw(self):
        self.graphicsContext.endDraw()

    def present(self, presenter):
        """Performs the rendering of the window and it's children to the windows graphic context.
        """
        if self.graphicsContext.getSize() != (self.width, self.height):
            # The size has changed since we last rendered, we need to resize the graphics context.
            # Note we only really need to do this when we redraw it, since creating and releasing
            # the context every time we get a window resize call may be very inefficient.
            self.graphicsContext.resize((self.width, self.height))

        # Draw the window first
        presenter.drawWidget("WINDOW", self, self.graphicsContext)

        # Draw each of the children on to the graphics context using the theme supplied through
        # the presenter
        for child in self.children:
            child.present(presenter, self.graphicsContext)

    def render(self):
        self.graphicsContext.render((self.posX, self.posY))

    def resize(self, w, h):
        Base.resize(self, w, h)
        self._panel.resize(w,h)

    def addDrawCallback(self, callback):
        self.drawLastCallbacks.append(callback)

    # for windows, children get added to the content panel
    def addChild(self, child, option = None):
        self._panel.addChild(child, option)
        child.calcSize()

    def move(self, x, y):
        Base.move(self, x,y)

    def moveto(self, x, y):
        Base.moveto(self, x,y)

    def setLayout(self, layout):
        self._panel.setLayout(layout)
        layout.setPanel(self._panel)

    def pack(self):
        self._panel.pack()

    def destroy(self):
        self._panel = None
        self.handle = 0
        self.drawList = []
        Base.destroy(self)

    def replacePanel(self, panel):
        for c in self.children:
            if c.id == self._panel.id:
                self.children.remove(c)

        self._panel = panel
        Base.addChild(self, self._panel)
        self._panel.setWindow(self)
        self.calcInnerRect()
        self.placeInnerObjects()
        self._panel.moveto(self.innerRect[0], self.innerRect[1])
        self._panel.resize(self.innerRect[2], self.innerRect[3])
        self._panel.calcInnerRect()
        self._panel.placeInnerObjects()

    def placeInnerObjects(self):
        self._panel.moveto(0,0)
        self._panel.resize(self.width, self.height)

    def setDirty(self, collide = 1):
        #self.dirty = 1
        if self.dirty:
            return
        if collide:
            getDesktop().dirtyCollidingWindows(self.rect)
        Base.setDirty(self)

    def setTopMost(self, value):
        if value == 0:
            self.topMost = 0
        else:
            self.topMost = 1
        #print "set topmost to ", self.topMost


    def setShow(self, value):
        if value:
            getDesktop().activateWindow(self)
        return Base.setShow(self, value)

    def isWindow(self):
        return True

    def desktopToWindow(self, point):
        """Convert a point in desktop coordinates into coordinates
            relative to the windows position.
        """
        x = int(point[0] - self.posX)
        y = int(point[1] - self.posY)
        return (x, y)

