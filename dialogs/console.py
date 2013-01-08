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

class ConsoleOutput:
    def __init__(self):
        self.lines = []
        self.oldout = sys.stdout
        self.olderr = sys.stderr
        
    def write(self, text):
        self.oldout.write("%s" % text)
        text = string.rstrip(text)
        if len(text) < 1:
            return
        text = string.replace(text, "\n", " ")
        text = string.replace(text, "\r", " ")      
        self.lines.append(text)
        getDesktop().postUserEvent(EVENT_OUTPUT)

    def beginCapture(self):
        sys.stdout = self
        sys.stderr = self

    def endCapture(self):
        sys.stdout = self.oldout
        self.stderr = self.olderr

    def getLines(self):
        return self.lines
    
    def clear(self):
        self.lines = []

    def __del__(self):
        self.endCapture()
        
#####################
# edit box with history
#####################
class ConsoleEdit(pyui2.widgets.Edit):
    def __init__(self, text, max, execCallback):
        pyui2.widgets.Edit.__init__(self, text, max, self._pyui2Enter)
        self.history = []
        self.historyPos = 0
        self.execCallback = execCallback
        self.registerEvent(locals.KEYDOWN, self._pyui2KeyDown)

    def _pyui2Enter(self, object):
        self.execCallback(self.text)
        self.history.append(self.text)
        self.historyPos = len(self.history) - 1
        self.setText("")
        self.setDirty()
        return 1

    def _pyui2KeyDown(self, event):
        if not self.hasFocus():
            return 0

        if event.key == locals.K_UP:
            if self.history:
                self.historyPos = (self.historyPos - 1) % len(self.history)
                self.setText(self.history[self.historyPos])
            return 1

        if event.key == locals.K_DOWN:
            if self.history:
                self.historyPos = (self.historyPos + 1) % len(self.history)
                self.setText(self.history[self.historyPos])
            return 1
                
        return pyui2.widgets.Edit._pyui2KeyDown(self, event)
    
#####################
# box to display lines of text for console output
# or chat windows...
####################
class LineDisplay(pyui2.widgets.Base):
    def __init__(self):
        pyui2.widgets.Base.__init__(self)
        #self.bgColor = (0,0,49, 255)
        self.lines = []
        self.displayLines = []
        font = getTheme().getProperty("DEFAULT FONT")
        self.numVisible = self.height / font.getTextSize("x")[1]
        self.numItems = 0
        self.topItem = 0
        self.rewrap = 0
        self.textWidth = 0
        self.vscroll = pyui2.widgets.VScroll()
        self.addChild(self.vscroll)
        self.registerEvent(locals.SCROLLPOS, self._pyui2ScrollPos)

    def clear(self):
        self.lines = []
        self.displayLines = []
        font = getTheme().getProperty("DEFAULT FONT")
        self.numVisible = self.height / font.getTextSize("x")[1]
        self.numItems = 0
        self.topItem = 0
        self.rewrap = 0

    def rewrapAll(self):
        self.displayLines = []
        for (line, color) in self.lines:
            self.wrapLine(line, color)
        numLines = len(self.displayLines)
        self.topItem = numLines - self.numVisible
        self.vscroll.setNumItems(numLines, self.numVisible)
        self.vscroll.scrollToItem(self.topItem)

    def wrapLine(self, line, color):
        """Add a line of text to the display lines list with wrapping."""
        (words, spaces) = self.splitLine(line)

        displayLine = ""
        width = 0
        space = ""
        spaceWidth = 0
        while words:
            word = words.pop(0)
            font = getTheme().getProperty("DEFAULT FONT")
            wordWidth = font.getTextSize(word)[0]

            if width + spaceWidth + wordWidth <= self.textWidth:
                displayLine = displayLine + space + word
                width += spaceWidth + wordWidth
            else:
                self.addDisplayLine(displayLine, color)
                displayLine = word
                width = wordWidth
            space = spaces.pop(0)
            font = getTheme().getProperty("DEFAULT FONT")
            spaceWidth = font.getTextSize(space)[0]
                
        if displayLine:
            self.addDisplayLine(displayLine, color)

    def splitLine(self, line):
        """Works like split(), but also returns whitespace between words"""
        words = []
        spaces = []
        nEnd = 0
        while nEnd < len(line):
            nStart = nEnd
            while nEnd < len(line) and not line[nEnd].isspace():
                nEnd += 1
            words.append(line[nStart:nEnd])
                
            nStart = nEnd
            nEnd += 1
            while nEnd < len(line) and line[nEnd].isspace():
                nEnd += 1
            spaces.append(line[nStart:nEnd])

        return (words,spaces)

    def addLine(self, line, color = None):
        """This adds lines to the display. it does text wrapping."""
        if not color:
            color = getTheme().fgColor
            
        self.lines.append((line, color))
        self.wrapLine(line, color)
        numLines = len(self.displayLines)
        self.topItem = numLines - self.numVisible
        self.vscroll.setNumItems(numLines, self.numVisible)
        self.vscroll.scrollToItem(self.topItem)

    def addDisplayLine(self, displayLine, color):
        self.displayLines.append((displayLine, color))
        self.setDirty()

#    def draw(self, renderer):
#        #renderer.drawRect(getTheme().bgColor2, self.windowRect)
#        if self.rewrap:
#            self.rewrapAll()
#            self.rewrap = 0
#            
#        i = 0
#        font = getTheme().getProperty("DEFAULT FONT")
#        h = font.getTextSize("x")[1]
#        for (line, color) in self.displayLines:
#            if i >= self.topItem and i < (self.topItem + self.numVisible):
#                renderer.drawText(line, (self.windowRect[0]+2, self.windowRect[1]+2+((i-self.topItem)*h)), color )
#            i += 1
#        self.vscroll.draw(renderer)
#        self.clearDirty()
#        
    def _pyui2ScrollPos(self, event):
        if event.id == self.vscroll.id:
            self.topItem = event.pos
            self.setDirty(1)

    def resize(self, w, h):
        pyui2.widgets.Base.resize(self, w,h)
        self.vscroll.resize(getTheme().getScrollerSize(), h)
        self.vscroll.moveto(w-getTheme().getScrollerSize(), 0)
        self.textWidth = self.width - self.vscroll.width
        font = getTheme().getProperty("DEFAULT FONT")
        self.numVisible = self.height / font.getTextSize("x")[1]
        self.rewrap = 1

    def destroy(self):
        self.vscroll.destroy()
        self.vscroll = None
        pyui2.widgets.Base.destroy(self)

####################################
# python console window
class Console(pyui2.widgets.Frame):

    def __init__(self, x, y, w, h, callback = None):
        pyui2.widgets.Frame.__init__(self, x, y, w, h, "Console")
        self.setLayout(pyui2.layouts.BorderLayoutManager())
        self.output = ConsoleOutput()
        self.locals = {}
        if not callback:
            callback = self._pyui2Go
            
        # create gui objects
        self.inputBox = ConsoleEdit("", 80, callback)
        self.goButton = pyui2.widgets.Button("Go", self._pyui2Go)
        self.outputBox = LineDisplay()

        self.panel = pyui2.widgets.Panel()
        self.panel.setLayout(pyui2.layouts.BorderLayoutManager())
        self.panel.addChild(self.inputBox, locals.CENTER)
        self.panel.addChild(self.goButton,locals.EAST)

        self.addChild(self.outputBox, locals.CENTER)
        self.addChild(self.panel, locals.SOUTH)
        self.panel.setWindow(self)
        self.pack()

        self.registerEvent(EVENT_OUTPUT, self._pyui2Output)

    def _pyui2Output(self, event):
        if not self.output:
            return 1
        lines = self.output.getLines()
        for l in lines:
            self.outputBox.addLine(l)
        self.output.clear()
        self.setDirty()
        return 1

    def _pyui2Go(self, command):
        self.output.beginCapture()
        try:
            print ">%s" % command
            exec command in globals(), self.locals
        except:
            print "Exception on command '%s':" % command
            print ">    %s" % sys.exc_value
        self.output.endCapture()
        return 1

    def destroy(self):
        #sys.stdout = None
        self.inputBox = None
        self.goButton = None
        self.outputBox = None
        self.panel = None
        pyui2.widgets.Frame.destroy(self)
        self.output = None

