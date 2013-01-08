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



class SliderBar(Base):
    """A horizontal slider bar. Has a slider handle that the user can drag to change its value.
    the onSlide method will be called when the value of the slider changes.
    """
    BARWIDTH = 8

    widgetLabel = "SLIDERBAR"

    def __init__(self, onSlide=None, range = 1, initialPos = 1):
        self.range = range
        self.position = initialPos
        self.sliding = 0
        self.slidePos = 0
        self.stepInterval = 1
        self._pyui2Slide = onSlide
        Base.__init__(self)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONUP, self._pyui2MouseUp)
        self.registerEvent(pyui2.locals.MOUSEMOVE, self._pyui2MouseMotion)

    def resize(self, w, h):
        Base.resize(self,w,h)
        self.stepInterval = (float(self.width) - self.BARWIDTH) / self.range

    def setRange(self, rnge):
        self.range = rnge
        self.resize(self.width, self.height)
        self.setDirty(1)

    def setValue(self, newValue):
        if newValue < 0 or newValue > self.range:
            return
        self.position = newValue
        self.setDirty(1)

    def _pyui2MouseDown(self, event):
        if not self.hit(event.pos):
            return 0
        if self.sliding:
            return 0

        adjEvtPos = self.convertToWindowCoords(event.pos)

        x = adjEvtPos[0] - self.posX
        barpos = int(self.stepInterval * self.position)

        #print "_pyui2MouseDown - hit success, adjEvtPos:", adjEvtPos, x, barpos

        if x > barpos and x < barpos + self.BARWIDTH:
            self.sliding = 1
            self.slidePos = x
            return 1
        return 0

    def _pyui2MouseUp(self, event):
        if not self.sliding:
            return 0
        self.sliding = 0
        return 1

    def _pyui2MouseMotion(self, event):
        if not self.sliding:
            return 0
        adjEvtPos = self.convertToWindowCoords(event.pos)

        x = adjEvtPos[0] - self.posX
        diff = x - self.slidePos
        newPosition = ((self.position * self.stepInterval) + diff) / self.stepInterval
        realdiff = newPosition - self.position
        if abs(realdiff) > 1:
            self.position = self.position + int(realdiff)
            if self.position < 0:
                self.position = 0
            if self.position >= self.range:
                self.position = self.range

            if self._pyui2Slide:
                self._pyui2Slide(self.position)

            self.slidePos = self.position * self.stepInterval
            self.setDirty(1)
            return 1
        return 0

