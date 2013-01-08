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
from dialog import Dialog


EVENT_OUTPUT = pyui2.desktop.getUserEvent()


class StdDialog(Dialog):
    def __init__(self, title, text):

        font = getTheme().getProperty("DEFAULT FONT")
        size = font.getTextSize(title)
        Dialog.__init__(self, title = title)
        self.setLayout(pyui2.layouts.BorderLayoutManager())

        self.textLabel = pyui2.widgets.Label(text)
        self.textLabel.setText(text)
        self.buttonPanel = pyui2.widgets.Panel()
        self.buttonPanel.setLayout(pyui2.layouts.BorderLayoutManager())
        self.okButton = pyui2.widgets.Button("OK", self._pyui2OK)
        self.okButton.resize(self.innerRect[2]/2, self.okButton.height)
        self.cancelButton = pyui2.widgets.Button("Cancel", self._pyui2Cancel)
        self.cancelButton.resize(self.innerRect[2]/2, self.cancelButton.height)     
        self.buttonPanel.addChild(self.okButton, locals.WEST)
        self.buttonPanel.addChild(self.cancelButton, locals.EAST)
        self.buttonPanel.pack()
        
        self.addChild(self.textLabel, locals.CENTER)
        self.addChild(self.buttonPanel, locals.SOUTH)

        self.pack()

    def _pyui2OK(self, button):
        self.close(1)

    def _pyui2Cancel(self, button):
        self.close(0)

    def draw(self, renderer):
        #print "drawing!!!"
        return Dialog.draw(self, renderer)

    def destroy(self):
        self.buttonPanel = None
        self.okButton = None
        self.cancelButton = None
        self.textLabel = None
        Dialog.destroy(self)

