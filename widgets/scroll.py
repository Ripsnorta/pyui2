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


class Scroll(Base):
    """Base scroll bar.
    """

    widgetLabel = "SCROLLBAR"

    def __init__(self):
        self.scrollPos = 0 # pixel position of scroll bar
        self.currentItem = 0
        self.status = 0
        self.barSize = 1
        self.barSpace = 1
        self.numItems = 1
        self.numVisible = 1
        self.interval = 1
        Base.__init__(self)
        self.setupBar()
        self.setupPos()
        self.start = 0
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONUP, self._pyui2MouseUp)
        self.registerEvent(pyui2.locals.MOUSEMOVE, self._pyui2MouseMotion)

    def setNumItems(self, numItems, numVisible):
        if numItems == 0:
            self.numItems = 1
        else:
            self.numItems = numItems
        self.numVisible = numVisible
        self.setupBar()
        self.setupPos()
        self.setDirty(1)

    def setupBar(self):
        if self.alignment == 'v':
            self.barSpace = self.height - (getTheme().getScrollerSize()*2 + 2)
        else:
            self.barSpace = self.width - (getTheme().getScrollerSize()*2 + 2)

        if self.barSpace < 1:
            self.barSpace = 1

        if self.numItems < self.numVisible:
            self.barSize = self.barSpace
        else:
            self.barSize = self.barSpace * self.numVisible / self.numItems
        if self.barSize < 5:
            self.barSize = 5

        if self.scrollPos > self.barSpace - self.barSize:
            self.scrollPos = max( self.barSpace - self.barSize, 0 )

    def setupPos(self):
        self.pos = getTheme().getScrollerSize() + 1 + self.scrollPos

        if self.barSpace == self.barSize:
            item = 0
        else:
            item = round((self.scrollPos/float((self.barSpace-self.barSize))) * (self.numItems-self.numVisible))

            if item >= self.numItems - self.numVisible:
                item = self.numItems - self.numVisible

        if item != self.currentItem:
            e = self.postEvent(pyui2.locals.SCROLLPOS)
            e.pos = int(item)
            self.currentItem = int(item)

    def resize(self, w, h):
        Base.resize(self, w, h)
        self.setupBar()
        self.setupPos()

    def calcSize(self):
        Base.calcSize(self)
        self.setupBar()
        self.setupPos()

    def scrollToItem(self, itemNum):
        #curr = (self.scrollPos/float(self.barSpace)) * self.numItems
        print "scrollToItem:", self.currentItem, itemNum, self.scrollPos
        if int(self.currentItem) != int(itemNum):
            self.scrollPos = (itemNum/float(self.numItems)) * float(self.barSpace)
            if self.scrollPos < 0:
                self.scrollPos = 0
            elif self.scrollPos > self.barSpace - self.barSize:
                self.scrollPos = self.barSpace - self.barSize
            self.setupPos()

    def _pyui2MouseDown(self, event):
        #print "_pyui2MouseDown:", event.pos, self.posX, self.posY, self.rect[2], self.rect[3]
        if not self.hit(event.pos):
            self.status = 0
            return 0

        adjEvtPos = self.convertToWindowCoords(event.pos)

        #localpos = (event.pos[0] - self.rect[0], event.pos[1] - self.rect[1])
        localpos = (adjEvtPos[0] - self.posX, adjEvtPos[1] - self.posY)
        #print "_pyui2MouseDown - hit success, localPos:", localpos

        scrollerSize = getTheme().getScrollerSize()

        if self.alignment == 'v':
            p = localpos[1]
            extent = self.height
        else:
            p = localpos[0]
            extent = self.width

        if p < scrollerSize:     # up button scroll
            if self.currentItem > 0:
                self.scrollToItem( self.currentItem - 1 )
            self.setDirty(1)
            return 1

        if p > extent - scrollerSize:    # down button scroll
            if self.currentItem < self.numItems:
                self.scrollToItem( self.currentItem + 1 )
            self.setDirty(1)
            return 1

        if self.pos < p < self.pos + self.barSize:     # <-- *** Just cleaned comparsion
            self.status = 1 # we are scrolling
            self.start = p
            self.setDirty(1)
            return 1
        else:     # unoccupied bar space
            self.scrollPos = p - scrollerSize - 1 - self.barSize/2    #center bar on cursor position
            if self.scrollPos < 0:
                self.scrollPos = 0
            elif self.scrollPos > self.barSpace - self.barSize:
                self.scrollPos = self.barSpace - self.barSize
            self.setupPos()
            self.status = 1
            self.start = p
            self.setDirty(1)
            return 1

    def _pyui2MouseUp(self, event):
        if not self.hit(event.pos):
            self.status = 0
            return 0
        self.status = 0

    def _pyui2MouseMotion(self, event):
        if self.status:
            localpos = (event.pos[0] - self.rect[0], event.pos[1] - self.rect[1])

            if self.alignment == 'v':
                p = localpos[1]
            else:
                p = localpos[0]

            diff = p - self.start
            self.scrollPos = self.scrollPos + diff
            if self.scrollPos < 0:
                self.scrollPos = 0
            elif self.scrollPos > self.barSpace - self.barSize:
                self.scrollPos = self.barSpace - self.barSize
            self.start = p
            self.setupPos()
            self.setDirty(1)
            return 1


class VScroll(Scroll):
    """Vertical scroll bar.
    """
    def __init__(self):
        self.alignment = 'v'
        Scroll.__init__(self)

class HScroll(Scroll):
    """Horizontal scroll bar.
    """
    def __init__(self):
        self.alignment = 'h'
        Scroll.__init__(self)

