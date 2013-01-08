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


class MenuBarWidget(Base):
    """Menu bar that fits at the top of a window.
    """
    border = 1
    def __init__(self):
        Base.__init__(self)
	self.resize( 0, getTheme().defaultTextHeight + 4 )
        self.setShow(1)
        self.menus = []
        self.hitList = []
        self.active = None
        self.highlight = None
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONUP, self._pyui2MouseUp)
        self.registerEvent(pyui2.locals.MOUSEMOVE, self._pyui2MouseMotion)
        self.registerEvent(pyui2.locals.MENU_EXIT, self._pyui2MenuExit)

       
    def addMenu(self, menu):
        self.menus.append(menu)

    def setActiveMenu(self, menu):
        if self.active:
            self.active.setShow(0)
        self.active = menu
        self.highlight = menu
        if ( menu ):
            menu.setShow(1)
        self.setDirty(1)

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
                self.setDirty(1)
        return 0
                
    def _pyui2MouseDown(self, event):
        # give active child first chance
        if self.active and self.active._pyui2MouseDown(event):
            return 1
        menu = self.findMenu(event.pos)
        if menu != self.active:
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
        x = pos[0] - self.rect[0]
        y = pos[1] - self.rect[1] + self.windowRect[1]
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
        Base.destroy(self)
