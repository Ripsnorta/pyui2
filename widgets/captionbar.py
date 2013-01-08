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

from pyui2.desktop import getDesktop, getTheme, getPresenter
from pyui2.base import Base
from pyui2.layouts import Much
from pyui2.widgets.button import Button


class CloseButton(Button):
    widgetLabel = "CLOSEBUTTON"

    def __init__(self, handler):
        Button.__init__(self, "", handler)


class MinimizeButton(Button):
    widgetLabel = "MINBUTTON"

    def __init__(self, handler):
        Button.__init__(self, "", handler)


class MaximizeButton(Button):
    widgetLabel = "MAXBUTTON"

    def __init__(self, handler):
        Button.__init__(self, "", handler)




class CaptionBar(Base):

    widgetLabel = "CAPTIONBAR"

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, text, closeBtn = True, minimizeBtn = False, maximizeBtn = False):
        Base.__init__(self)
        self.setText(text)
        self.closeBtn = closeBtn
        self.minimizeBtn = minimizeBtn
        self.maximizeBtn = maximizeBtn
        self.moving = False
        self.mouseDown = False
        self.captionCursorSet = False

        self._closeBtn = None
        if self.closeBtn == True:
            self._closeBtn = CloseButton(self.onCloseButton)
            self.addChild(self._closeBtn)

        self._minimizeBtn = None
        if self.minimizeBtn == True:
            self._minimizeBtn = MinimizeButton(self.onMinimizeButton)
            self.addChild(self._minimizeBtn)

        self._maximizeBtn = None
        if self.maximizeBtn == True:
            self._maximizeBtn = MaximizeButton(self.onMaximizeButton)
            self.addChild(self._maximizeBtn)


        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONUP, self._pyui2MouseUp)
        self.registerEvent(pyui2.locals.MOUSEMOVE, self._pyui2MouseMotion)

    #########################################################################################################
    ##
    #########################################################################################################
    def getPreferredSize(self):
        font = getTheme().getAggProperty(("CAPTIONBAR", "TITLE", "font"))
        if font == None:
            font = getTheme().getDefaultFont()
            
        (width, height) = font.getTextSize(self.text)
        return self.width, height

    #########################################################################################################
    ##
    #########################################################################################################
    def getMaximumSize(self):
        return Much, self.getPreferredSize()[1]

    #########################################################################################################
    ##
    #########################################################################################################
    def setButton(self, button, rect, justification):

        (newX, newY, newW, newH) = rect
        if button != None:

            width = rect[3]
            y = rect[1]

            if justification == "left":
                x = rect[0]
                newX = x + width
            else:
                x = rect[0] + rect[2] - width

            newW = newW - width

            button.moveto(x, y)
            button.resize(width, width)

        return (newX, newY, newW, newH)
    
    #########################################################################################################
    ##
    #########################################################################################################
    def placeInnerObjects(self):
        btnJust = getTheme().getAggProperty(("CAPTIONBAR", "BUTTONS", "justified"))
        if btnJust == None:
            btnJust = "right"

        rect = (self.posX, self.posY, self.width, self.height)
        rect = self.setButton(self._closeBtn, rect, btnJust)
        rect = self.setButton(self._maximizeBtn, rect, btnJust)
        rect = self.setButton(self._minimizeBtn, rect, btnJust)

        self.textRect = rect

    #########################################################################################################
    ##
    #########################################################################################################
    def moveto(self, x, y):
        """move to absolute position.
        """
        Base.moveto(self, x, y)
        self.placeInnerObjects()

    #########################################################################################################
    ##
    #########################################################################################################
    def move(self, dx, dy):
        """move relative to current position.
        """
        Base.move(self, dx, dy)
        self.placeInnerObjects()

    #########################################################################################################
    ##
    #########################################################################################################
    def resize(self, w, h):
        """ resize absolute size of the widget
        """
        Base.resize(self, w, h)
        self.placeInnerObjects()

    #########################################################################################################
    ##
    #########################################################################################################
    def setText(self, text):
        """Set the text of the label. sets the dirty flag.
        """
        self.text = text
        if len(text) == 0:
            text = " "

        (self.width, self.height) = self.getPreferredSize()
        self.setDirty()

    #########################################################################################################
    ##
    #########################################################################################################
    def getHeight(self):
        return self.windowRect[3]

    #########################################################################################################
    ##
    #########################################################################################################
    def present(self, presenter, graphicsContext):
        """Performs the rendering of the panel and it's children to the windows graphic context.
        """
        # Draw the panel first
        presenter.drawWidget("CAPTIONBAR", self, graphicsContext)

        for child in self.children:
            child.present(presenter, graphicsContext)

    #########################################################################################################
    ##
    #########################################################################################################
    def handleEvent(self, event):
        """ do menu, then panel
        """
        if not self.show:
            return

        # The captionbar is a composite widget, it not only consists of the
        # bar, but also of buttons, icons, or a system menu.
        if self._minimizeBtn:
            if self.minimizeBtn.handleEvent(event):
                return 1

        if self._maximizeBtn:
            if self._maximizeBtn.handleEvent(event):
                return 1

        if self._closeBtn:
            if self._closeBtn.handleEvent(event):
                return 1

        if self.eventMap.has_key(event.type):
            if self.eventMap[event.type](event):
                return 1

        return 0

    #########################################################################################################
    ##
    #########################################################################################################
    def _pyui2MouseMotion(self, event):
        if self.parent.moveable and self.hit(event.pos):
            if self.moving:
                mouseX = event.pos[0] - self.posX
                mouseY = event.pos[1] - self.posY
    
                # The parent of a captionbar should always be a frame, this may fail if
                # it is not.
                self.parent.frameMove(mouseX - self.startX, mouseY - self.startY)
                (self.startX, self.startY) = (mouseX, mouseY)

            if self.mouseDown == True:
                getTheme().setMovingCursor()
            else:
                getTheme().setButtonCursor()

            self.captionCursorSet = True    
            return 1
        else:
            if self.captionCursorSet == True:
                self.captionCursorSet = False
                getTheme().setArrowCursor()
            return 0
        
    #########################################################################################################
    ##
    #########################################################################################################
    def _pyui2MouseDown(self, event):
        if not self.hit(event.pos):
            return 0

        self.mouseDown = True
        self.moving = True
        self.startX = event.pos[0] - self.posX
        self.startY = event.pos[1] - self.posY
        return 1

    #########################################################################################################
    ##
    #########################################################################################################
    def _pyui2MouseUp(self, event):
        self.mouseDown = False
        self.moving = False

        if not self.hit(event.pos):
            return 0
        return 1

    #########################################################################################################
    ##
    #########################################################################################################
    def onCloseButton(self, data):
        if self.parent != None:
            self.parent.frameClose()

    #########################################################################################################
    ##
    #########################################################################################################
    def onMinimizeButton(self, data):
        pass

    #########################################################################################################
    ##
    #########################################################################################################
    def onMaximizeButton(self, data):
        pass