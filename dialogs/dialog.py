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

import sys
import re
import os, stat
import string

import pyui2
from pyui2 import locals
from pyui2.desktop import getDesktop, getTheme


EVENT_OUTPUT = pyui2.desktop.getUserEvent()


##################################
# Dialog
#
##################################
class Dialog(pyui2.widgets.Frame):
    def __init__(self, x = -1, y = -1, w = 300, h = 200, title = None):
        # center if position not specified
        if x < 0:
            x = (getDesktop().width - w) / 2
        if y < 0:
            y = (getDesktop().height - h) / 2
        pyui2.widgets.Frame.__init__(self, x, y, w, h, title)
        self.modal = -1   # this is set to the return value of the dialog
        self.setShow(1)
        self.setDirty()
        self.cb = None
        
    def doModal(self, cb = None):
        self.setShow(1)
        self.cb = cb
        getDesktop().setModal(self)

    def close(self, value = 1):
        #print "closed - " , value
        self.modal = value
        getDesktop().setModal(None)
        self.setShow(0)
        self.loseFocus()
        self.postEvent(locals.DIALOGCLOSED)
        pyui2.desktop.getTheme().setArrowCursor()
        if self.cb:
            self.cb(value)

    def destroy(self):
        if getDesktop().getModal() == self:
            getDesktop().setModal(None)
        pyui2.widgets.Frame.destroy(self)

