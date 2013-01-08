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
from pyui2.window import Window
from pyui2.layouts import Much


class MenuItem:
    """Used by menu widget to track items. Can have an icon 16x16 in size.
    """
    def __init__(self, handler, text, subMenu):
        self.handler = handler
        self.text = text
        font = getTheme().getAggProperty(("MENU","font"))
        if font == None:
            font = getTheme().getProperty("DEFAULT FONT")

        (width, height) = font.getTextSize(text)
        self.width = width
        self.subMenu = subMenu
        self.icon = None
        self.rect = (0,0,0,0)
        self.canActivate = handler or subMenu

    def setIcon(self, icon):
        self.icon = icon

class Menu(Window):
    """Menu that can be floating or attached to a menuBar.
    """
    widgetLabel = "MENU"

    iconWidth = 20  # fixme[pmf]: actually defined in theme
    minWidth = 20
    border = 4
    def __init__(self, title):
        Window.__init__(self, 0,0,100,100, topmost = 1)
        self.menuTitle = title
        self.width = self.minWidth
        self.items = []
        self.active = None
        self.subActive = None
        self.setShow(0)

        # no register events; we'll receive events from the menu bar (or other parent menu)

    def present(self, presenter):
        """Performs the rendering of the window and it's children to the windows graphic context.
        """
        if self.graphicsContext.getSize() != (self.width, self.height):
            # The size has changed since we last rendered, we need to resize the graphics context.
            # Note we only really need to do this when we redraw it, since creating and releasing
            # the context every time we get a window resize call may be very inefficient.
            self.graphicsContext.resize((self.width, self.height))

        # Draw the window first
        presenter.drawWidget("MENU", self, self.graphicsContext)

    def calcItemRects(self):
        font = getTheme().getAggProperty(("MENU","font"))
        if font == None:
            font = getTheme().getProperty("DEFAULT FONT")

        x = self.border
        y = self.border
        for item in self.items:
            (width, height) = font.getTextSize(item.text)
            item.rect = (x, self.posY + y, width, height)
            y = y + height

    def setShow(self, show):
        if show:
            self.getFocus()
            self.recalcSize()

        if self.subActive:
            self.subActive.setShow(0)

        self.subActive = None
        self.active = None
        Base.setShow(self,show)

    def addItem(self, title, handler = None, subMenu = None):
        """Add an item to the menu.
        """
        if subMenu:
            title = title + "..."
        newItem = MenuItem(handler, title, subMenu)
        self.items.append(newItem)
        self.recalcSize()
        self.calcItemRects()
        self.setDirty()

        return newItem

    def recalcSize(self):
        font = getTheme().getAggProperty(("MENU","font"))
        if font == None:
            font = getTheme().getProperty("DEFAULT FONT")

        (width, height) = font.getTextSize("Wp")

        h = height * 1.3 * len(self.items) + self.border * 2
        w = self.minWidth
        for item in self.items:
            if item.width > w:
                w = item.width
        self.resize(w + self.iconWidth * 2 + self.border * 2, h)

    def changeItemTitle(self, oldTitle, newTitle, newHandler):
        for item in self.items:
            if item.text == oldTitle:
                item.text = newTitle
                item.handler = newHandler
                self.setDirty(1)
                break

    def setActive(self, item):
        if item == self.active:
            return

        if self.subActive:
            self.subActive.setShow(0)

        # can't use menu items without an event attached
        if item and not item.canActivate:
            self.active = None
            return

        self.active = item
        if item:
            self.subActive = item.subMenu
            if self.subActive:
                self.activateSubmenu(item)

        self.setDirty()

    def findItem(self, pos):
        if not self.hit(pos):
            return None

        adjEvtPos = self.convertToWindowCoords(pos)

        # put hit position in window relative coords
        x = adjEvtPos[0] - self.posX
        y = adjEvtPos[1] - self.posY
        for item in self.items:
            if x >= item.rect[0] and y >= item.rect[1] and x < item.rect[0]+item.rect[2] and y < item.rect[1]+item.rect[3]:
                return item
        return None

    def _pyui2MouseMotion(self, event):
        # give active submenu first chance
        if self.subActive and self.subActive._pyui2MouseMotion(event):
            return 1
        item = self.findItem(event.pos)
        if item and item != self.active:
            self.setActive(item)
        return item != None

    def _pyui2MouseDown(self, event):
        # give active submenu first chance
        if self.subActive and self.subActive._pyui2MouseDown(event):
            return 1
        item = self.findItem(event.pos)
        if item != self.active:
            self.setActive(item)
        return item != None

    def _pyui2MouseUp(self, event):
        # give active submenu first chance
        if self.subActive and self.subActive._pyui2MouseUp(event):
            return 1
        item = self.findItem(event.pos)
        if item != self.active:
            self.setActive(item)
        if not item:
            return 0
        if item.subMenu:
            return 1
        if not item.canActivate:
            return 1
        print "picked menu item:", item.text
        if item.handler:
            item.handler(item)
        #e = self.postEvent(item.eventType)
        #e.item = item
        self.postEvent(pyui2.locals.MENU_EXIT)
        return 1

    def activateSubmenu(self, item):
        self.subActive = item.subMenu
        (x,y) = (self.posX + item.rect[2], self.posY + item.rect[1] - self.border)
        if x + item.subMenu.width > getDesktop().width:
            # try moving to left of menu
            x -= self.width + item.subMenu.width
            if x < 0:
                # the menu won't fit, nor to the left of the parent menu, nor to the right. What to do?
                # Align the submenu to the right margin.
                x = getDesktop().width - item.subMenu.width
                item.subMenu.moveto(getDesktop().width - item.subMenu.width, self.posY + item.subMenu.height * getTheme().getStyle("menu").getTextHeight())

        if y + item.subMenu.height > getDesktop().height:
            y = getDesktop().height - item.subMenu.height
            if y < 0:
                raise "No room for submenu!"
        item.subMenu.moveto(x, y)
        item.subMenu.setShow(1)



class MenuPopup(Menu):
    """Menu that can be floating or attached to a menuBar.
    """
    def __init__(self):
        Menu.__init__(self, "")
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.RMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONUP, self._pyui2MouseUp)
        self.registerEvent(pyui2.locals.MOUSEMOVE, self._pyui2MouseMotion)
        self.registerEvent(pyui2.locals.MENU_EXIT, self._pyui2MenuExit)

    def activate(self, x, y):
        # can set up context sensitive stuff here.
        self.moveto(x, y)
        self.setShow(1)

    def _pyui2MenuExit(self, event):
        if self.show:
            self.setShow(0)
            return 1
        return 0

    def _pyui2MouseMotion(self, event):
        if self.show:
            return Menu._pyui2MouseMotion(self, event)
        return 0

    def _pyui2MouseDown(self, event):
        if self.show:
            if Menu._pyui2MouseDown(self, event):
                return 1
            self.setShow(0)
        return 0

    def _pyui2MouseUp(self, event):
        if self.show:
            if Menu._pyui2MouseUp(self, event):
                return 1
        return 0


class MenuBar(Window):
    """Menu bar that fits at the top of the screen or the top of a window.
    """
    widgetLabel = "MENUBAR"
    border = 1
    def __init__(self):
        w = getDesktop().width
        font = getTheme().getAggProperty(("MENU","font"))
        if font == None:
            font = getTheme().getProperty("DEFAULT FONT")

        (width, height) = font.getTextSize("Wp")

        Window.__init__(self, 0,0, w, height * 1.3, topmost = 1)
        self.setShow(1)
        self.menus = []
        self.hitList = []
        self.active = None
        self.highlight = None
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONUP, self._pyui2MouseUp)
        self.registerEvent(pyui2.locals.MOUSEMOVE, self._pyui2MouseMotion)
        self.registerEvent(pyui2.locals.MENU_EXIT, self._pyui2MenuExit)

    def present(self, presenter):
        """Performs the rendering of the window and it's children to the windows graphic context.
        """
        if self.graphicsContext.getSize() != (self.width, self.height):
            # The size has changed since we last rendered, we need to resize the graphics context.
            # Note we only really need to do this when we redraw it, since creating and releasing
            # the context every time we get a window resize call may be very inefficient.
            self.graphicsContext.resize((self.width, self.height))

        # Draw the window first
        presenter.drawWidget("MENUBAR", self, self.graphicsContext)


    def calcHitList(self):
        font = getTheme().getAggProperty(("MENU","font"))
        if font == None:
            font = getTheme().getProperty("DEFAULT FONT")

        height = self.height - (2 * self.border)
        x = self.posX + self.border
        print "We have %d menus"%len(self.menus)
        for menu in self.menus:
            width = int(font.getTextSize(menu.menuTitle)[0] * 1.33)
            rect = (x, self.posY, width, height)
            menu.moveto(x, self.posY + height)
            print "Calculating the menu at:", menu.posX, menu.posY
            self.hitList.append((menu, rect))
            x = x + width

        
    def addMenu(self, menu):
        self.menus.append(menu)
        self.calcHitList()

    def setActiveMenu(self, menu):
        if self.active:
            self.active.setShow(0)

        self.active = menu
        self.highlight = menu
        if menu:
            #print self.posX + self.border, self.posY + self.height
            #menu.moveto(self.posX + self.border, self.posY + self.height)
            menu.setShow(1)

        self.setDirty()

    def _pyui2MenuExit(self, event):
        if self.active:
            self.setActiveMenu(None)
            return 1
        return 0

    def _pyui2MouseMotion(self, event):
        # give active child first chance
        if self.active and self.active._pyui2MouseMotion(event):
            return 1
        menu = self.findMenu(event.pos)
        if self.active:
            if menu and menu != self.active:
                self.setActiveMenu(menu)
        else:
            if menu != self.highlight:
                self.highlight = menu
                self.setDirty()
        return 0

    def _pyui2MouseDown(self, event):
        # give active child first chance
        if self.active and self.active._pyui2MouseDown(event):
            return 1
        menu = self.findMenu(event.pos)
        if menu != None:
            self.setActiveMenu(menu)
            return 1

        return 0

    def _pyui2MouseUp(self, event):
        # give active child first chance
        if self.active and self.active._pyui2MouseUp(event):
            return 1
        menu = self.findMenu(event.pos)
        if self.active and not menu:
            self.setActiveMenu(None)
            return 1
        return 0

    def setParent(self, parent):
        Base.setParent(self, parent)

    def findMenu(self, pos):
        if not self.hit(pos):
            return None

        # put hit position in window relative coords
        x = pos[0] - self.posX
        y = pos[1] - self.posY
        for (menu, rect) in self.hitList:
            if x >= rect[0] and y >= rect[1] and x < rect[0]+rect[2] and y < rect[1]+rect[3]:
                return menu
        else:
            return None

    def destroy(self):
        for menu in self.menus:
            menu.destroy()
            del menu
        self.menus = None
        self.hitList = None
        Window.destroy(self)
