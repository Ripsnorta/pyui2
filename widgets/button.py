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
from pyui2.base import Base
from pyui2.layouts import Much


class Button(Base):
    """button object. has a text label. Handler will be called when it is pressed.
    """

    widgetLabel = "BUTTON"

    IDLE = 0
    ROLLOVER = 1
    DOWN = 2

    canTab = 1

    def __init__(self, text, handler = None, font=None, shadow=0, fgColor=None, bgColor=None, roColor=None):
        Base.__init__(self)
        self.handler = handler
        self.font=font
        self.shadow=shadow
        self.fgColor=fgColor
        self.bgColor=bgColor
        self.roColor=roColor

        self.setText(text)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONUP, self._pyui2MouseUp)
        self.registerEvent(pyui2.locals.KEYDOWN, self._pyui2KeyDown)
        self.registerEvent(pyui2.locals.KEYUP, self._pyui2KeyUp)
        self.registerEvent(pyui2.locals.MOUSEMOVE, self._pyui2MouseMotion)
        self.registerEvent(pyui2.locals.CLICKED, self._pyui2Clicked)
        self.status = Button.IDLE
        self.capture = 0
        self.enabled = 1
        self.tooltipText = text


    def getPreferredSize(self):
        if self.font:
            font = self.font
        else:
            font = getTheme().getDefaultFont()

        size = font.getTextSize("  "+self.text+"  ")
        size = size[0], int(size[1] * 1.5)
        return size

    def getMaximumSize(self):
        return Much, self.getPreferredSize()[1]


    def setText(self, text, dontResize=0):
        """Pass 1 to dontResize if you dont want the button to resize itself to the
        text passed in.
        """
        self.text = text
        if len(text) < 1:
            text = " "

        if not dontResize:
            width, height = self.getPreferredSize()
            self.resize(width, height)

    def getText(self):
        return self.text

    def _pyui2Clicked(self, event):
        if event.id == self.id and self.handler:
            self.handler(self)
            return 1
        return 0

    def _pyui2MouseMotion(self, event):
        if self.capture:
            if self.hit(event.pos):
                if self.status != Button.DOWN:
                    self.status = Button.DOWN
                    self.setDirty()
            else:
                if self.status == Button.DOWN:
                    self.status = Button.ROLLOVER
                    self.setDirty()
            return 1

        if self.hit(event.pos):
            #print "button got mouse move:", event.pos, self.rect, self.posX, self.posY
            if self.status != Button.ROLLOVER:
                getDesktop().getTheme().setButtonCursor()
                self.status = Button.ROLLOVER
                self.setDirty()
                return 0
        else:
            if self.status == Button.ROLLOVER:
                getDesktop().getTheme().setArrowCursor()
                self.status = Button.IDLE
                self.setDirty()
                return 0
        return 0

    def _pyui2MouseDown(self, event):
        #print "Mouse Down at", event.pos, "button rect =", self.rect
        if not self.hit(event.pos):
            return 0
        if not self.enabled:
            return 1
        #print "Setting Status"
        self.status = Button.DOWN
        self.getFocus()
        self.capture = 1
        self.setDirty()
        return 1

    def _pyui2MouseUp(self, event):
        #print "Mouse Up"
        if self.capture:
            self.capture = 0
            if self.status == Button.DOWN and self.enabled:
                self.postEvent(pyui2.locals.CLICKED)
                self.status = Button.IDLE
                self.setDirty()
            return 1
        return 0

    def _pyui2KeyDown(self, event):
        if not self.hasFocus():
            return 0
        if event.key == pyui2.locals.K_SPACE and self.enabled:
            self.status = Button.DOWN
            self.setDirty()
            return 1
        return 0

    def _pyui2KeyUp(self, event):
        if not self.hasFocus():
            return 0
        if event.key == pyui2.locals.K_SPACE and self.enabled:
            self.postEvent(pyui2.locals.CLICKED)
            self.status = Button.IDLE
            self.setDirty()
            return 1
        return 0

    def enable(self):
        self.enabled = 1
        self.setDirty(1)

    def disable(self):
        self.enabled = 0
        self.setDirty(1)



class ImageButton(Button):
    """Same as regular button except it has an image instead of text.
    """

    widgetLabel = "IMAGEBUTTON"

    def __init__(self, filename, handler, selectFilename = "", mouseOverFilename="", border=False, text = ""):
        self.filename = filename
        self.selectFilename = selectFilename
        self.mouseOverFilename = mouseOverFilename
        self.border = border
        Button.__init__(self, text, handler)

    def maxSize(self, a, b):
        if a[0] >= b[0]:
            sz[0] = a[0]
        else:
            sz[0] = b[0]

        if a[1] >= b[1]:
            sz[1] = a[1]
        else:
            sz[1] = b[1]

        return sz

    def getPreferredSize(self):
        normalImageSize = getPresenter().getImageSize(self.filename)
        selectImageSize = getPresenter().getImageSize(self.selectFilename)
        mouseoImageSize = getPresenter().getImageSize(self.mouseOverFilename)
        
        # Return the largest of the three
        imageSize = self.maxSize(normalImageSize, selectImageSize)
        imageSize = self.maxSize(imageSize, mouseoImageSize)
        return imageSize

    def getMaximumSize(self):
        return Much, self.getPreferredSize()[1]

    def setFilename(self, filename):
        self.filename = filename
        self.setDirty(1)

    def setSelectFilename(self, filename):
        self.selectFilename = filename
        self.setDirty(1)

    def setMouseOverFilename(self, filename):
        self.mouseOverFilename = filename
        self.setDirty(1)

    def setBorder(self, border):
        self.border = border
        self.setDirty(1)
