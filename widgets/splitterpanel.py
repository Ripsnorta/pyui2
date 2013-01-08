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

from pyui2.desktop import getDesktop, getTheme
from pyui2.panel import Panel
from pyui2.layouts import Much


class SplitterPanel(Panel):
    """A panel that is split in half - vertically or horizontally.
    Can use pixels or percentage to split. Each side of the split is a panel.
    The default panels can be replaced with custom panels.

    There is a middle bar of the splitter panel. This middle bar _could_ be used
    to resize it...
    """

    VERTICAL = 0
    HORIZONTAL = 1

    PIXELS = 0
    PERCENTAGE = 1

    PADDING = 2
    
    def __init__(self, direction = VERTICAL, method = PERCENTAGE, ratio = 50 ):
        self.direction = direction  # vertical/horizontal
        self.method = method        # pixels/percentage
        self.ratio = ratio          # number of pixels or percentage
        self.splitPos = 0           # pixel width/height of first panel
        if self.method == SplitterPanel.PERCENTAGE:
            self.ratio = float(ratio) / 100.0
        Panel.__init__(self)
        self.panel1 = Panel()
        self.panel2 = Panel()
        self.addChild(self.panel1)
        self.addChild(self.panel2)

    def setVerticalSplit(self, x):
        self.panel1.moveto(0,0)
        self.panel1.resize(x-self.PADDING, self.height)
        self.panel2.moveto(x+self.PADDING, 0)
        self.panel2.resize(self.width-x-self.PADDING, self.height)
        self.splitPos = x

    def setHorizontalSplit(self, y):
        self.panel1.moveto(0,0)
        self.panel1.resize(self.width, y-self.PADDING)
        self.panel2.moveto(0, y+self.PADDING)
        self.panel2.resize(self.width, self.height-y-self.PADDING)
        self.splitPos = y

    def resize(self, w, h):
        Base.resize(self, w,h)
        #print "splitter resizing", w, h
        if self.method == SplitterPanel.PIXELS:
            if self.direction == SplitterPanel.VERTICAL:
                if self.ratio >= 0:
                    self.setVerticalSplit(self.ratio)
                else:
                    self.setVerticalSplit(self.width + self.ratio)
            if self.direction == SplitterPanel.HORIZONTAL:
                if self.ratio >= 0:
                    self.setHorizontalSplit(self.ratio)
                else:
                    self.setHorizontalSplit(self.height + self.ratio)
        else:
            if self.direction == SplitterPanel.VERTICAL:
                self.setVerticalSplit(self.width * self.ratio)
            if self.direction == SplitterPanel.HORIZONTAL:
                self.setHorizontalSplit(self.height * self.ratio)

    def draw(self, renderer):
        self.panel1.draw(renderer)

        if self.direction == SplitterPanel.HORIZONTAL:
            getTheme().drawSplitter(
                                 (self.windowRect[0], self.windowRect[1]+self.splitPos-self.PADDING, self.width, self.PADDING*2))
        else:
            getTheme().drawSplitter(            
                                 (self.windowRect[0]+self.splitPos-self.PADDING, self.windowRect[1], 2*self.PADDING, self.height))
            
        self.panel2.draw(renderer)
        
    def pack(self):
        self.panel1.pack()
        self.panel2.pack()
        
    def getFirstPanel(self):
        """ returns the left or top panel
        """
        return self.panel1

    def getSecondPanel(self):
        """ returns to right or bottom panel
        """
        return self.panel2

    def replaceFirstPanel(self, panel):
        panel.moveto(self.panel1.posX, self.panel1.posY)
        for c in self.children:
            if c.id == self.panel1.id:
                self.children.remove(c)
                c.destroy()
        self.addChild(panel)
        self.panel1 = panel
        self.resize(self.width, self.height)
        
    def replaceSecondPanel(self, panel):
        panel.moveto(self.panel2.posX, self.panel2.posY)
        for c in self.children:
            if c.id == self.panel2.id:
                self.children.remove(c)
                c.destroy()
        self.addChild(panel)
        self.panel2 = panel
        self.resize(self.width, self.height)
