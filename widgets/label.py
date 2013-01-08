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


class Label(Base):
    """Label object has a text label. uses default font if font is not specified.
    """

    widgetLabel = "LABEL"

    LEFT   = 0
    CENTER = 1
    RIGHT  = 2

    def __init__(self, text, color = None, font = None, shadow=0, align=0):
        Base.__init__(self)
        self.font = font
        self.shadow = shadow
        self.align = align
        self.color = color
        self.setText(text)
        self.border = False

    def getPreferredSize(self):
        if self.font:
            font = self.font
        else:
            font = getTheme().defaultFont

        return font.getTextSize(self.text)

    getMaximumSize = getPreferredSize

    def setText(self, text):
        """Set the text of the label. sets the dirty flag.
        """
        if self.font:
            font = self.font
        else:
            font = getTheme().defaultFont

        self.text = text
        if len(text) == 0:
            text = " "
        (self.width,self.height) = font.getTextSize(text)
        self.setDirty()

    def setColor(self, color = None):
        self.color = color
        self.setDirty()

    def setShadow(self, shadow=True):
        self.shadow = shadow
        self.setDirty()

    def setAlignment(self, alignment=0):
        self.align = alignment
        self.setDirty()

    def setBorder(self, border=True):
        self.border = border
        self.setDirty

