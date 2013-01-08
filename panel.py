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
from pyui2.desktop import getDesktop, getTheme
from pyui2 import layouts


class Panel(Base):
    """Used for handling interior window drawing and layouts.
    This is the simplest type of panel that other are derived from.
    """
    widgetLabel = "PANEL"

    def __init__(self):
        Base.__init__(self)
        self.childOptions = {}
        self.widgetIDs = {}
        self.registerEvent(pyui2.locals.KEYDOWN, self._pyui2KeyDown)
        self.setLayout(layouts.FlowLayoutManager())

    def setLayout(self, layout):
        self.layout = layout
        self.layout.setPanel(self)

    def present(self, presenter, graphicsContext):
        """Performs the rendering of the panel and it's children to the windows graphic context.
        """
        # Draw the panel first
        presenter.drawWidget(self.widgetLabel, self, graphicsContext)

        # Draw each of the children on to the graphics context using the theme supplied through
        # the presenter
        for child in self.children:
            child.present(presenter, graphicsContext)

    def getWidget(self, widgetID):
        widget = None

        for child in self.children:
            if child.widgetID == widgetID:
                widget = child

        return widget

    def getFocus(self):
        self.nextTab()

    def nextTab(self, step = 1):
        # see if a child currently has focus
        for i in xrange(len(self.children)):
            if self.children[i].hasFocus():
                tab = i + step
                break
        else:
            tab = 0

        for i in xrange(0, len(self.children)):
            tab = tab % len(self.children)
            child = self.children[tab]

            if isinstance(child, Panel) and child.nextTab(step):
                break

            if child.canTab:
                break

            tab += step
        else:
            return 0
        self.children[tab].getFocus()
        return 1

    def _pyui2KeyDown(self, event):
        if event.key == pyui2.locals.K_TAB:
            if event.mods & pyui2.locals.MOD_SHIFT:
                self.nextTab(-1)
            else:
                self.nextTab(+1)
            return 0
        #print "Unhandled key in panel:", event.key
        return 0

    def createChildID(self, child):
        if self.widgetIDs.has_key(child.widgetLabel):
            idNum = self.widgetIDs[child.widgetLabel]
        else:
            idNum = 0

        child.setID(child.widgetLabel + "_" + str(idNum))

        idNum = idNum + 1

        self.widgetIDs[child.widgetLabel] = idNum

    def addChild(self, child, option = None):
        if child.getID() == "":
            self.createChildID(child)

        Base.addChild(self, child)
        self.childOptions[child.id] = option

        if child.width > self.width:
            self.width = child.width
        if child.height > self.height:
            self.height = child.height
        # panel cannot be larger than parent
        if self.parent:
            if self.width > self.parent.width:
                self.width = self.parent.width
            if self.height > self.parent.height:
                self.height = self.parent.height

    def pack(self):
        self.layout.begin(self)
        for child in self.children:
            self.layout.scanChild(child, self.childOptions[child.id])

        for child in self.children:
            self.layout.placeChild(child, self.childOptions[child.id])
            child.pack()

        self.layout.end()

    def resize(self, w, h):
        Base.resize(self, w, h)
        self.pack()

    def destroy(self):
        del self.layout
        self.layout = None
        Base.destroy(self)


    def listChildIDs(self):
        print "Listing children IDs"

        for child in self._panel.children:
            print child.widgetID

        print ""

