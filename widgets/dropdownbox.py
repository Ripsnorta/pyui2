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
from pyui2.widgets.listbox import ListBox


class DropDownBox(Base):
    """A drop-down selection box. Pass the number of lines to be visible in the drop-down
    list to the constructor.
    """
    BUTTON_WIDTH = 10
    DEFAULT_WIDTH = 10

    widgetLabel = "DROPDOWN"

    def __init__(self, numVisible = 5, onSelected = None, listItems = None, selection = None, editable = True):
        Base.__init__(self)
        self.numVisible = numVisible
        self.selectionList = ListBox(self._pyui2SelectedEvent)
        self.selectionList.setShow(0)
        self.addChild(self.selectionList)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.selectHandler = onSelected
        self.addItems(listItems)
        self.setSelectedItem(selection)

    def getPreferredSize(self):
        font = getTheme().getProperty("DEFAULT FONT")
        size = font.getTextSize("W" * self.DEFAULT_WIDTH)
        return int(size[0]), int(size[1])

    def getMaximumSize(self):
        return Much, self.getPreferredSize()[1]

    ## pass-through methods to the list box

    def addItem(self, itemText, itemData, color = None):
        self.selectionList.addItem(itemText, itemData, color)
        #self.selectionList.selected = len(self.selectionList.items) - 1

    def addItems(self, itemList, color = None):
        if itemList != None:
            for itemText, itemData in itemList:
                self.selectionList.addItem(itemText, itemData, color)

            #self.selectionList.selected = len(self.selectionList.items) - 1

    def setSelectedItem(self, selection):
        if selection != None:
            if selection >= 0 and selection < len(self.selectionList.items):
                self.selectionList.selected = selection

    def getSelectedItem(self):
        return self.selectionList.getSelectedItem()

    def removeItem(self, text):
        self.selectionList.removeItem(text)

    def clearSelection(self):
        self.selectionList.clearSelection()

    def clear(self):
        self.selectionList.clear()


    def present(self, presenter, graphicsContext):
        presenter.drawWidget(self.widgetLabel, self, graphicsContext)

        for child in self.children:
            child.present(presenter, graphicsContext, (self.posX, self.posY, self.windowRect[2], self.windowRect[3]))

    def hideMe(self, interval):
        if self.selectHandler:
            self.selectHandler(self.item)
        self.selectionList.setShow(0)
        return 1

    def resize(self, width, height):
        Base.resize(self, width, height)
        self.positionSelectionList()

    def positionSelectionList(self):
        font = getTheme().getProperty("DEFAULT FONT")

        self.selectionList.resize(self.width, self.numVisible * font.getTextSize("x")[1])
        self.selectionList.moveto(self.posX, self.posY + self.height)

    def handleEvent(self, event):
        if not self.show:
            return

        if self.selectionList.handleEvent(event):
            return 1

        if self.eventMap.has_key(event.type):
            if self.eventMap[event.type](event):
                return 1
        return 0

    def _pyui2MouseDown(self, event):
        if not self.hit(event.pos):
            if self.selectionList.show:
                self.selectionList.setShow(0)
            return 0

        adjEvtPos = self.convertToWindowCoords(event.pos)

        x = adjEvtPos[0] - self.posX
        y = adjEvtPos[1] - self.posY
        if x > self.width - self.rect[3] and x < self.width:
            if self.selectionList.show == 0:
                self.positionSelectionList()
                self.selectionList.setShow(1)
            else:
                self.selectionList.setShow(0)
        return 1

    def _pyui2SelectedEvent(self, item):
        self.item = item
        getDesktop().addCallback(self.hideMe, 0.33)
        return 1


