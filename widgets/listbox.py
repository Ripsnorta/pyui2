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
from pyui2.widgets.scroll import VScroll


class ListBoxItem:
    """Used by ListBox to track items.
    """
    def __init__(self, name, data, fg, bg):
        self.name = name
        self.data = data
        self.color = fg

class ListBox(Base):
    """List Box has a scrollable list of selectable items.
       List box behavior should incorporate the right mouse button -BrianU 10-31-02
    """
    canTab = 1
    widgetLabel = "LISTBOX"

    def __init__(self, onSelected = None, onDouble = None):
        Base.__init__(self)
        self.items = []
        if self.font:
            font = self.font
        else:
            font = getTheme().defaultFont

        self.numVisible = self.height / ( font.getTextSize("x")[1] )
        self.numItems = 0
        self.topItem = 0
        self.selected = -1
        self.vscroll = VScroll()
        self.addChild(self.vscroll)
        self.registerEvent(pyui2.locals.SCROLLPOS, self._pyui2ScrollPos)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2LButtonDown)
        self.registerEvent(pyui2.locals.RMOUSEBUTTONDOWN, self._pyui2LButtonDown)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONUP, self._pyui2LButtonUp)
        self.registerEvent(pyui2.locals.RMOUSEBUTTONUP, self._pyui2LButtonUp)
        self.registerEvent(pyui2.locals.LMOUSEDBLCLICK, self._pyui2DoubleClick)

        self.registerEvent(pyui2.locals.LIST_SELECTED, self._pyui2SelectEvent)
        self.registerEvent(pyui2.locals.LIST_DBLCLICK, self._pyui2DoubleEvent)

        self.resize(100,100)

        self.selectHandler = onSelected
        self.doubleHandler = onDouble

    def clearAllItems(self):
        self.items = []
        if self.font:
            font = self.font
        else:
            font = getTheme().defaultFont
        self.numVisible = self.height /  (font.getTextSize("x")[1] )
        self.numItems = 0
        self.topItem = 0
        self.selected = -1

    def populateList(self, items):
        for item in items:
            self.addItem(item, None)
        self.sortByName()

    def addItem(self, itemText, itemData, color = None):
        """add an item to the list box. the data value is stored for the item
        and will be available when events occur on that item.
        """
        item = ListBoxItem(itemText, itemData, color, color)
        self.items.append(item)
        self.numItems = len(self.items)
        self.vscroll.setNumItems(self.numItems, self.numVisible)
        self.setDirty()

    def removeItem(self, itemText):
        i = 0
        for item in self.items:
            if item.name == itemText:
                if i <= self.selected:
                    self.selected -= 1
                self.items.pop(i)
                #print "removed %s" % itemText
                break
            #print itemText, item.name
            i = i + 1
        self.numItems = len(self.items)
        self.vscroll.setNumItems(self.numItems, self.numVisible)
        self.setDirty()

    def removeItemByData(self, itemData):
        i = 0
        for item in self.items:
            if item.data == itemData:
                if i <= self.selected:
                    self.selected -= 1
                self.items.pop(i)
                break
            i = i + 1
        self.numItems = len(self.items)
        self.vscroll.setNumItems(self.numItems, self.numVisible)
        self.setDirty()

    def getItemByData(self, itemData):
        for item in self.items:
            if item.data == itemData:
                return item
        return None

    def present(self, presenter, graphicsContext, parentRect=None):
        presenter.drawWidget(self.widgetLabel, self, graphicsContext, parentRect)

        offsetX = 0
        offsetY = 0
        if parentRect != None:
            offsetX = parentRect[0]
            offsetY = parentRect[1]

        for child in self.children:
            child.present(presenter, graphicsContext, (self.posX+offsetX, self.posY+offsetY, self.windowRect[2], self.windowRect[3]))


    def getSelectedItem(self):
        if self.selected > -1 and self.selected < len(self.items):
            return self.items[self.selected]
        return None

    def setSelectedItem(self, name):
        i=0
        for item in self.items:
            if item.name == name:
                self.selected = i
                self.setDirty()
                break
            i = i + 1

    def resize(self, w, h):
        Base.resize(self, w, h)
        if self.font:
            font = self.font
        else:
            font = getTheme().defaultFont
        self.numVisible = int (self.height / font.getTextSize("x")[1] )
        self.vscroll.setNumItems(self.numItems, self.numVisible)
        self.vscroll.resize(getTheme().getScrollerSize(), h)
        self.vscroll.moveto(self.posX + w - getTheme().getScrollerSize(), self.posY)

    def clearSelection(self):
        self.selected = -1
        self.setDirty()

    def clear(self):
        self.items = []
        self.numItems = 0
        self.vscroll.setNumItems(0, self.numVisible)
        self.selected = -1
        self.setDirty()

    def sortByName(self):
        self.items.sort(self.itemCompareByName)
        self.setDirty()

    def sortByData(self):
        self.items.sort(self.itemCompareByData)
        self.setDirty()

    def itemCompareByName(self, item1, item2):
        return cmp(item1.name, item2.name)

    def itemCompareByData(self, item1, item2):
        return cmp(item1.data, item2.data)

    def handleEvent(self, event):
        if not self.show:
            return

        # The listbox is a composite widget, it not only consists of the
        # list, but also a scrollbar.
        if self.vscroll.handleEvent(event):
            return 1

        if self.eventMap.has_key(event.type):
            if self.eventMap[event.type](event):
                return 1
        return 0

    def _pyui2ScrollPos(self, event):
        if event.id == self.vscroll.id:
            self.topItem = event.pos
            self.setDirty()

    def _pyui2LButtonDown(self, event):
        if not self.hit(event.pos):
            return 0

        adjEvtPos = self.convertToWindowCoords(event.pos)

        if self.font:
            font = self.font
        else:
            font = getTheme().defaultFont
        item =  int( (adjEvtPos[1] - self.posY) / font.getTextSize("x")[1] )
        self.selected = item + self.topItem
        self.postEvent(pyui2.locals.LIST_SELECTED)
        self.setDirty()
        return 0

    def _pyui2LButtonUp(self, event):
        return 0

    def _pyui2DoubleClick(self, event):
        if not self.hit(event.pos):
            return 0

        adjEvtPos = self.convertToWindowCoords(event.pos)

        if self.font:
            font = self.font
        else:
            font = getTheme().defaultFont
        item =  int( (adjEvtPos[1] - self.posY) / font.getTextSize("x")[1] )
        self.selected = item + self.topItem
        self.postEvent(pyui2.locals.LIST_DBLCLICK)
        self.setDirty()
        return 1

    def _pyui2SelectEvent(self, event):
        if event.id == self.id:
            if self.selectHandler:
                self.selectHandler( self.getSelectedItem() )
                return 1
        return 0

    def _pyui2DoubleEvent(self, event):
        if event.id == self.id:
            if self.doubleHandler:
                self.doubleHandler( self.getSelectedItem() )
                return 1
        return 0

