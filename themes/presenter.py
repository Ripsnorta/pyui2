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
from pyui2.system import DCX
from pyui2.desktop import getDesktop

class Presenter:
    cursors = {}
    methods = {}

    def __init__(self, width, height, fullscreen = False):
        self.width          = width
        self.height         = height
        self.fullscreen     = fullscreen
        self.cursorName     = None
        self.mousePosition  = None
        self.backDraw       = None
        self.mustFill       = 0


    def setDeviceContext(self, device):
        pyui2.system.setDeviceContext(device)


    def getDeviceContext(self):
        return pyui2.system.getDeviceContext()


    def getScreenSize(self):
        return self.width, self.height

    def determineDeviceContext(self, deviceName):
        """Takes a string representing the required device and
            rendering capabilities and creates a Device Context.
        """
        if deviceName == "2d":
            from pyui2.system.pygamedevice import PygameDevice
            self.setDeviceContext(PygameDevice(self.width, self.height, self.fullscreen, PygameDevice.P2D))

        elif deviceName == "p3d":
            from pyui2.system.pygamedevice import PygameDevice
            self.setDeviceContext(PygameDevice(self.width, self.height, self.fullscreen, PygameDevice.OGL))

        elif deviceName == "gl":
            from pyui2.system.glutdevice import GLUTDevice
            self.setDeviceContext(GLUTDevice(self.width, self.height, self.fullscreen))


    def setTheme(self, theme):
        self.theme = theme
        self.theme.setPresenter(self)
        self.theme.setupTheme()


    def setBackgroundDrawing(self, backDraw):
        self.backDraw = backDraw


    def setDrawingMethod(self, id, method):
        self.methods[id] = method


    def draw(self, id, rect, params):
        return self.methods[id](rect, params)


    def drawWidget(self, widgetName, widget, graphicsContext, parentRect=None):
        self.theme.draw(widgetName, widget, graphicsContext, parentRect)


    def loadMouseCursor(self, mouseCursor, offset, cursorName):
        image = self.getDeviceContext().loadImage(mouseCursor)
        self.cursors[cursorName] = (image, offset)
        #print self.cursors


    def setCurrentMouseCursor(self, cursorName):
        self.cursorName = cursorName


    def setMousePosition(self, position):
        self.mousePosition = position


    def drawMouseCursor(self):
        if self.mousePosition != None:
            #print "drawMouseCursor"
            try:
                image, offset = self.cursors[self.cursorName]
                pyui2.system.getDeviceContext().drawImage(image, (self.mousePosition[0] - offset[0], self.mousePosition[1] - offset[1]) )
            except KeyError:
                print "Mouse cursor,", self.cursorName, "not defined"
                #print self.cursors


    def setMustFill(self):
        self.mustFill = 1

    def getMustFill(self):
        return self.mustFill

    def present(self, windows):
        desktop = getDesktop()
        if desktop and desktop.running:
            if self.backDraw != None:
                self.backDraw()
            else:
                pyui2.system.getDeviceContext().clearScreen()

            pyui2.system.getDeviceContext().prepare()

            for window in reversed(windows):
                if window.show:
                    if window.dirty or self.mustFill == 1:
                        window.beginDraw()
                        window.present(self)
                        window.endDraw()
                        window.clearDirty()

                    window.render()

            self.drawMouseCursor()

            if self.mustFill == 1:
                self.mustFill = 0

            pyui2.system.getDeviceContext().present()

    def dirtyCollidingWindows(self, inRect):
        """If a dirty rect collides with any other rects, they should be dirty also. This recurses
        so that all colliding rects get dirtied. the second parameter to setDirty() prevents infinite
        recursion.
        """
        pass

    def collideRects(self, rect1, rect2):
        return rect2[0] < rect1[0] + rect1[2] and rect2[0] + rect2[2] > rect1[0] and rect2[1] < rect1[1] + rect1[3] and rect2[1] + rect2[3] > rect1[1]

    def loadImage(self, filename, label = None):
        return pyui2.system.getDeviceContext().loadImage(filename, label)

    def getImage(self, filename, label = None, reloadImage=False):
        return pyui2.system.getDeviceContext().getImage(filename, label, reloadImage)

    def getImageSize(self, filename, label = None):
        return pyui2.system.getDeviceContext().getImageSize(filename, label)




