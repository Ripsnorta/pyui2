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
from pyui2.panel import Panel
from pyui2.base import Base
from pyui2.layouts import Much
from pyui2.widgets.button import Button



class TabScrollButton(Button):
    widgetLabel = "TABSCROLLBUTTON"

    DIRECT_LEFT = 0
    DIRECT_RIGHT = 1
    DIRECT_UP = 2
    DIRECT_DOWN = 3

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, direction, handler):
        Button.__init__(self, "", handler)

        self.direction = direction





#############################################################################################################
##
#############################################################################################################
class TabButton(Button):
    widgetLabel = "TABBUTTON"

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, text, handler, selected=False):
        Button.__init__(self, text, handler)
        self.selected = selected

    #########################################################################################################
    ##
    #########################################################################################################
    def getPreferredSize(self):
        font = getTheme().getAggProperty(("TABBUTTON", "font"))
        if font == None:
            font = getTheme().getProperty("DEFAULT FONT")

        (width, height) = font.getTextSize(self.text)
        return int(width * 1.5), int(height * 1.3)

    #########################################################################################################
    ##
    #########################################################################################################
    def select(self):
        self.selected = True

    #########################################################################################################
    ##
    #########################################################################################################
    def unselect(self):
        self.selected = False



#############################################################################################################
##
#############################################################################################################
class TabBar(Base):
    """The TabBar is a widget that manages the tab buttons used by the Tabbed Panel
        widget.
    """
    widgetLabel = "TABBAR"

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, callback):
        Base.__init__(self)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.KEYDOWN, self._pyui2KeyDown)
        self.callback = callback
        self.activeTab = None
        self.lScroll = TabScrollButton(TabScrollButton.DIRECT_LEFT, self.moveTabsLeft)
        self.rScroll = TabScrollButton(TabScrollButton.DIRECT_RIGHT, self.moveTabsRight)
        self.addChild(self.lScroll)
        self.addChild(self.rScroll)
        self.needScrollButtons = False
        self.tabButtons = []
        self.firstVisibleTab = 0

    #########################################################################################################
    ##
    #########################################################################################################
    def calcInnerRect(self):
        left = self.posX
        top = self.posY
        width = self.width
        height = self.height

        self.innerRect = (left, top, width, height)
        #print "TabBar::calcInnerRect:", self.innerRect

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
        #print "TabBar::placeInnerObjects:", self.innerRect

        rect = (self.posX, self.posY, self.width, self.height)
        rect = self.setButton(self.rScroll, rect, "right")
        rect = self.setButton(self.lScroll, rect, "right")

        self.tabRect = rect

        x = rect[0]
        y = self.posY

        for tabButton in self.tabButtons:
            tabButton.show = 0

        idx = self.firstVisibleTab
        iEnd = len(self.tabButtons)
        while idx < iEnd:
            tabButton = self.tabButtons[idx]
            if (x + tabButton.width + 2) <= (rect[0] + rect[2]):
                tabButton.show = 1
                tabButton.moveto(x, y)
                x += tabButton.width + 2
            else:
                break

            idx += 1

    #########################################################################################################
    ##
    #########################################################################################################
    def getHeight(self):
        return self.windowRect[3]

    #########################################################################################################
    ##
    #########################################################################################################
    def addTab(self, tabLabel):
        tabButton = TabButton(tabLabel, self.onClick)
        buttonHeight = tabButton.getPreferredSize()[1]

        if buttonHeight > self.height:
            self.resize(self.width, buttonHeight)

        self.addChild(tabButton)
        self.tabButtons.append(tabButton)

        totalWidth = 0
        for btn in self.tabButtons:
            totalWidth += btn.width

        if totalWidth > self.width:
            self.needScrollButtons = True
        else:
            self.needScrollButtons = False

        if self.activeTab == None:
            self.activeTab = tabButton
            self.activeTab.select()

    #########################################################################################################
    ##
    #########################################################################################################
    def present(self, presenter, graphicsContext):
        """Performs the rendering of the panel and it's children to the windows graphic context.
        """
        # Draw the panel first
        presenter.drawWidget("TABBAR", self, graphicsContext)

        if self.needScrollButtons:
            self.lScroll.present(presenter, graphicsContext)
            self.rScroll.present(presenter, graphicsContext)

        for tabButton in self.tabButtons:
            tabButton.present(presenter, graphicsContext)

    #########################################################################################################
    ##
    #########################################################################################################
    def nextTab(self):
        nextTabButton = self.activeTab

        if self.activeTab != None:
            activeIndex = self.children.index(self.activeTab)
        else:
            activeIndex = -1

        activeIndex += 1

        if activeIndex <= len(self.tabButtons) - 1:
            nextTabButton = self.tabButtons[activeIndex]

        self.onClick(nextTabButton)

    #########################################################################################################
    ##
    #########################################################################################################
    def prevTab(self):
        prevTabButton = self.activeTab

        if self.activeTab != None:
            activeIndex = self.tabButtons.index(self.activeTab)
        else:
            activeIndex = len(self.tabButtons)

        activeIndex -= 1

        if activeIndex >= 0:
            prevTabButton = self.tabButtons[activeIndex]

        self.onClick(prevTabButton)

    #########################################################################################################
    ##
    #########################################################################################################
    def handleEvent(self, event):
        if not self.show:
            return

        for child in self.children:
            if child.handleEvent(event):
                return 1

        if self.eventMap.has_key(event.type):
            if self.eventMap[event.type](event):
                return 1
        return 0

    #########################################################################################################
    ##
    #########################################################################################################
    def moveTabsLeft(self, data):
        #print "Tab Left"
        self.firstVisibleTab -= 1
        if self.firstVisibleTab < 0:
            self.firstVisibleTab = 0

        self.placeInnerObjects()
        self.setDirty()

    #########################################################################################################
    ##
    #########################################################################################################
    def moveTabsRight(self, data):
        #print "moveTabsRight"
        idx = self.firstVisibleTab
        iEnd = len(self.tabButtons)
        totalWidth = 0
        while idx < iEnd:
            tabButton = self.tabButtons[idx]
            btnWidth = tabButton.width + 2
            totalWidth += btnWidth

            #print "TabButton:", tabButton.text, tabButton.width, btnWidth, totalWidth, self.tabRect[2]

            if totalWidth > self.tabRect[2]:
                #print "Tab Right"
                self.firstVisibleTab += 1
                if self.firstVisibleTab > iEnd - 1:
                    self.firstVisibleTab = iEnd - 1
                break

            idx += 1

        self.placeInnerObjects()
        self.setDirty()

    #########################################################################################################
    ##
    #########################################################################################################
    def _pyui2MouseDown(self, event):
        pass

    #########################################################################################################
    ##
    #########################################################################################################
    def _pyui2KeyDown(self, event):
        if event.key == pyui2.locals.K_TAB:
            #print event.key, event.mods
            if event.mods == 1:
                self.prevTab()
            else:
                self.nextTab()

            return 1
        return 0

    #########################################################################################################
    ##
    #########################################################################################################
    def onClick(self, tabButton):
        #print tabButton.text, "clicked"
        if self.activeTab != tabButton:
            self.activeTab.unselect()
            self.activeTab = tabButton
            self.activeTab.select()

            self.onTabChange(self.activeTab.text)

    #########################################################################################################
    ##
    #########################################################################################################
    def onTabChange(self, tabLabel):
        if self.callback != None:
            self.callback(tabLabel)


#############################################################################################################
##
#############################################################################################################
class TabbedPanel(Panel):
    """A panel with multiple panels that are activated by tabs along the top of the panel.
    The inner panels can be created by this panel or existing panels can be added in.
    """
    #tabsHeight = getTheme().defaultTextHeight + 8

    widgetLabel = "TABBEDPANEL"

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self):
        Panel.__init__(self)
        self._tabBar = TabBar(self.onTabChange)
        self._tabBar.setWindow(self.window)
        self._tabBar.setParent(self)
        self.activePanel = None
        self.tabPanels = {}             # mapping of titles to panels
        self.activePanel = None
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.KEYDOWN, self._pyui2KeyDown)
        self.calcInnerRect()
        self.placeInnerObjects()

    def setWindow(self, window):
        Panel.setWindow(self, window)
        self._tabBar.setWindow(self.window)

    #########################################################################################################
    ##
    #########################################################################################################
    def placeInnerObjects(self):
        self.moveto(self.innerRect[0], self.innerRect[1])
        self.resize(self.innerRect[2], self.innerRect[3])

        tabHeight = 0
        if self._tabBar != None:
            self._tabBar.moveto(self.innerRect[0], self.innerRect[1])
            self._tabBar.resize(self.innerRect[2], self._tabBar.rect[3])
            tabHeight = self._tabBar.getHeight()
            self._tabBar.calcInnerRect()
            self._tabBar.placeInnerObjects()

        for panel in self.children:
            panel.moveto(self.innerRect[0], self.innerRect[1]+tabHeight)
            panel.resize(self.innerRect[2], self.innerRect[3]-tabHeight)


    #########################################################################################################
    ##
    #########################################################################################################
    def calcInnerRect(self):
        left = self.posX
        top = self.posY
        width = self.windowRect[2]
        height = self.windowRect[3]

        self.innerRect = (left, top, width, height)

        if self._tabBar != None:
            self._tabBar.calcInnerRect()


    #########################################################################################################
    ##
    #########################################################################################################
    def onTabChange(self, tabLabel):
        self.activePanel = self.tabPanels[tabLabel]
        self.activePanel.setDirty()
        self.setDirty()


    #########################################################################################################
    ##
    #########################################################################################################
    def removePanel(self, title):
        """Remove an existing panel by its name.
        """
        self.removeChild(self.tabPanels[title])
        del self.tabPanels[title]

    #########################################################################################################
    ##
    #########################################################################################################
    def addPanel(self, title, panel = None):
        """Can add an existing panel, or have a panel created by default.
        Adding an existing panel is useful for adding special panel types (splitters/tabs)
        """
        if not panel:
            panel = Panel()

        self.addChild(panel)
        panel.moveto(self.innerRect[0], self.innerRect[1])
        panel.resize(self.innerRect[2], self.innerRect[3])
        panel.calcSize()

        panel.tabTitle = title
        self.tabPanels[title] = panel
        self._tabBar.addTab(title)

        if not self.activePanel:
            self.activePanel = panel
            self.setDirty()

        return panel

    #########################################################################################################
    ##
    #########################################################################################################
    def getPanel(self, number):
        return self.children[number]

    #########################################################################################################
    ##
    #########################################################################################################
    def findPanel(self, tabLabel):
        return self.tabPanels[tabLabel]

    #########################################################################################################
    ##
    #########################################################################################################
    def resize(self, w, h):
        """Only resize the current tab. other tabs are resized when switched to later if it is required."""
        #print "tabbed panel resizing ", w, h, self
        Panel.resize(self, w, h)
        self.calcInnerRect()

    #########################################################################################################
    ##
    #########################################################################################################
    def pack(self):
        # dont pack self.. just pack the child panels.
        for p in self.children:
            p.pack()


    #########################################################################################################
    ##
    #########################################################################################################
    def present(self, presenter, graphicsContext):
        """Performs the rendering of the panel and it's children to the windows graphic context.
        """
        # Draw the panel first
        presenter.drawWidget("TABBEDPANEL", self, graphicsContext)

        if self.activePanel:
            self.activePanel.present(presenter, graphicsContext)

        if self._tabBar:
            self._tabBar.present(presenter, graphicsContext)


    #########################################################################################################
    ##
    #########################################################################################################
    def activatePanel(self, p):
        if p != self.activePanel:
            for panel in self.children:
                if panel == p:
                    panel.setShow(1)
                else:
                    panel.setShow(0)

            self.activePanel = p

            # move and resize the tab if required.
            if p.width != self.width or p.height != self.height:
                p.resize(self.width, self.height)

            self.setDirty()
            p.getFocus()


    #########################################################################################################
    ##
    #########################################################################################################
    def nextPanel(self):
        for i in range(0,len(self.children)):
            if self.children[i] == self.activePanel:
                if i == len(self.children)-1:
                    #print "activating" , 0, self.children[0]
                    self.activatePanel(self.children[0])
                    break
                else:
                    #print "activating" , i, self.children[i+1]
                    self.activatePanel(self.children[i+1])
                    break


    #########################################################################################################
    ##
    #########################################################################################################
    def handleEvent(self, event):
        if not self.show:
            return
        if self._tabBar:
            if self._tabBar.handleEvent(event):
                return 1
        if self.activePanel.handleEvent(event):
            return 1
        if self.eventMap.has_key(event.type):
            if self.eventMap[event.type](event):
                return 1
        return 0

    #########################################################################################################
    ##
    #########################################################################################################
    def _pyui2MouseDown(self, event):
        if not self.hit(event.pos):
            return 0
        self.getFocus()
        return 0

    #########################################################################################################
    ##
    #########################################################################################################
    def _pyui2KeyDown(self, event):
        if event.mods & pyui2.locals.MOD_CONTROL:
            if event.key == pyui2.locals.K_TAB:
                self.nextPanel()
                return 1
            number = event.key - ord('0') - 1
            if number >= 0 and number < 10:
                if number < len(self.children):
                    self.activatePanel(self.children[number])
                    return 1

        return 0

    #########################################################################################################
    ##
    #########################################################################################################
    def getFocus(self):
        # hand off focus to active panel
        if self.activePanel:
            self.activePanel.getFocus()

    #########################################################################################################
    ##
    #########################################################################################################
    def checkHit(self, pos):
        if pos[0] > self.rect[0] and \
           pos[0] < self.rect[0] + self.rect[2] and \
           pos[1] > self.rect[1] and \
           pos[1] < self.rect[1] + self.rect[3]:

            result = self.activePanel.checkHit(pos)
            if result:
                return result
            return self
        else:
            return None

