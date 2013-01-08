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

veri = 0

import pyui2
from pyui2.desktop import getDesktop, getTheme
from pyui2 import layouts
#from window import Window

class Base:
    """Base GUI object that all other drawable object derive from.
    this object implements:
        - containment of other GUI objects
        - position and size
        - event handling
        - unique identity of all GUI objects

    self.rect is in absolute co-ordinates, self.windowRect is in relative window co-ordinates.
    self.posX and self.posY are relative to the parent object
    """
    widgetLabel = "BASE"

    def __init__(self):
        """Initialize and register the base widget. widgets are added to the global widget list initially.
        """
        self.canTab = 0     # this widget acts as a tab stop
        self.widgetID = ""
        self.parent = None
        self.window = None
        self.posX = 0
        self.posY = 0
        self.width = 1
        self.height = 1
        self.show = 1
        self.dirty = 1
        self.children = []
        self.eventMap = {}
        self.calcSize()
        getDesktop().registerWidget(self)
        self.popup = None
        self.tooltipText = ""
        self.font = None


#    def hit(self, pos):
#        """Check for a hit using absolute coordinates.
#        """
#        #if self.rect[0] < pos[0] < self.rect[0] + self.rect[2] and self.rect[1] < pos[1] < self.rect[1] + self.rect[3]:
#        if self.rect[0] < pos[0] < self.rect[0] + self.rect[2] and self.rect[1] > pos[1] > self.rect[1] - self.rect[3]:
#            return 1
#        else:
#            return 0

    def getParentWindow(self, par):
        while par != None:
            if issubclass(par.__class__, pyui2.window.Window):
                return par
            par = par.parent
        return None

    def convertToWindowCoords(self, pos):
        newPos = pos
        win = self.getParentWindow(self.parent)
        if win != None:
            newPos = win.desktopToWindow(pos)
        return newPos

    def hit(self, pos):
        """Check for a hit adjusting the position relative to the parent window.
        """
        adjPos = self.convertToWindowCoords(pos)
        rect = (self.posX, self.posY, self.rect[2], self.rect[3])

        #print "hitRel: pos =", pos,  "adjPos =", adjPos, "rect=", rect

        if rect[0] < adjPos[0] < rect[0] + rect[2] and rect[1] < adjPos[1] < rect[1] + rect[3]:
            return 1
        else:
            return 0

    def isWindow(self):
        return False

    def getFocus(self):
        """Acquire the gui system's focus. only one Base may have the focus
        """
        #if isinstance(self, Window):
        if self.isWindow():
            getDesktop().activateWindow(self)
        else:
            getDesktop().activateWindow(self.window)
        getDesktop().setFocus(self)
        self.setDirty()

    def loseFocus(self):
        """lose the gui system's focus.
        """
        getDesktop().setFocus(None)
        self.setDirty()

    def hasFocus(self):
        return getDesktop().getFocus() == self

    def postEvent(self, eventType):
        """Post an event to be processed next time through the event loop
        """
        if getDesktop():
            return getDesktop().postEvent(eventType, self.id)


    def calcSize(self):
        """This sets up self.rect to be absolute co-ordinates. also sets up self.windowRect
        to be relative to the upper left of the parent Window
        """
        (x, y) = (self.posX, self.posY)
        p = self.parent
        while p and not p.isWindow(): #isinstance(p, Window):
            x += p.posX
            y += p.posY
            p = p.parent

        if self.window:
            self.rect = (x + self.window.posX, y + self.window.posY, self.width, self.height)
            self.windowRect = (x, y, self.width, self.height)
        else:
            self.rect = (self.posX, self.posY, self.width, self.height)
            self.windowRect = (0, 0, self.width, self.height)

        for child in self.children:
            child.calcSize()

    def getPreferredSize(self):
        """Determine the recommended size for this widget.
        This size should never be the value 'Much'.
        """
        return (self.width, self.height)

    def getMaximumSize(self):
        """Determine the recommended maximum size for this widget
        """
        return (layouts.Much, layouts.Much)

    def addChild(self, child):
        """Add a child widget.
        """
        self.children.append(child)
        child.setWindow(self.window)
        child.setParent(self)

    def removeChild(self, child):
        try:
            self.children.remove(child)
            child.setParent(None)
            return child
        except:
            print "ERROR: couldn't find the child to remove."
            return None

    def addPopup(self, popup):
        ### arg... dont know about popups here..
        ### assert isinstance(popup, MenuPopup)
        self.popup = popup

    def setParent(self, parent):
        """Set the parent of this widget
        """
        self.parent = parent

    def setWindow(self, window):
        self.window = window
        for child in self.children:
            child.setWindow(window)

    def present(self, presenter, graphicsContext, parentRect=None):
        presenter.drawWidget(self.widgetLabel, self, graphicsContext, parentRect)

    def handleEvent(self, event):
        """ event processing for base objects
        """
        if not self.show:
            return
        i = len(self.children) - 1
        while i > -1:
            child = self.children[i]
            if child.handleEvent(event):
                #print child, "handled", event.type
                return 1
            i = i  - 1
        if self.eventMap.has_key(event.type):
            if self.eventMap[event.type](event):
                #print self, "handled", event.type
                return 1

        # popup handling here so it's not overridden with subclass event behavior
        if self.popup and event.type == pyui2.locals.RMOUSEBUTTONDOWN and self.hit(event.pos):
            self.popup.activate(event.pos[0], event.pos[1])
            return 1
        return 0

    def moveto(self, x, y):
        """move to absolute position.
        """
        self.posX = x
        self.posY = y
        self.calcSize()

    def move(self, dx, dy):
        """move relative to current position.
        """
        self.posX = self.posX + dx
        self.posY = self.posY + dy
        self.calcSize()

    def resize(self, w, h):
        """ resize absolute size of the widget
        """
        self.setDirty()
        self.width = w
        self.height = h
        self.calcSize()

    def registerEvent(self, eventType, handler):
        """Setup handler for an event
        """
        self.eventMap[eventType] = handler

    def unregisterEvent(self, eventType):
        """Remove handler for an event
        """
        if self.eventMap.has_key(eventType):
            del self.eventMap[eventType]

    def pack(self):
        """used by panels & layout managers
        """
        pass

    def setDirty(self, collide = 1):
        """Sets this widget to redraw itself and notifies window.
        """
        self.dirty = 1
        if self.window:
            self.window.setDirty()

    def clearDirty(self):
        """Clears this widgets dirty flag.
        """
        self.dirty = 0

    def setID(self, widgetID):
        self.widgetID = widgetID

    def getID(self):
        return self.widgetID


    def destroy(self):
        """Call this to remove all references to the widget from the system.
        """
        #print "destroying %s (%d)" % (self, self.id)
        self.window = None
        self.setParent(None)
        if self.popup:
            self.popup.destroy()
            self.popup = None
        if self.children:
            for child in self.children:
                child.destroy()
            self.children = []
        self.eventMap.clear()
        getDesktop().destroyWidget(self)

    def setShow(self,value):
        self.show = value
        self.setDirty()
        for child in self.children:
            child.setShow(value)
        if not value:
            getDesktop().getTheme().setArrowCursor()

    def __del__(self):
        #print "Deleting widget %s (%d)" % (self, self.id)
        pass

    def getToolTipInfo(self, pos):
        """return a tuple of the text and rectangle for the tooltip for when the
        mouse is in <pos> within the window. This uses the member variable toolTipInfo
        if it is populated.
        """
        if self.tooltipText:
            return (self.tooltipText,  (pos[0]-50, pos[1]-20, 120, 30) )
        else:
            return None

    def checkHit(self, pos):
        if not self.show:
            return None
        if self.hit(pos):
            for child in self.children:
                result = child.checkHit(pos)
                if result:
                    return result
            return self
        else:
            return None


