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


class Edit(Base):
    """Edit box. accepts input from user. some emacs-like editing functionality.
    """
    canTab = 1     

    widgetLabel = "EDIT"       

    def __init__(self,text, maxSize, handler = None, readOnly = 0):
        Base.__init__(self)
        self.handler = handler
        self.caretPos = None
        self.selectPos = None
        self.setText(text)        
        self.dragging = 0
        self.maxSize = maxSize
        self.readOnly = readOnly

        self.font = getTheme().getAggProperty(("EDIT", "font"))
        if self.font == None:
            self.font = getTheme().getProperty("DEFAULT FONT")

        self.resize(self.width, int(self.font.getTextSize("x")[1] * 1.5) )
        #print "Edit widget sized to", self.width, self.height
        self.registerEvent(pyui2.locals.KEYDOWN, self._pyui2KeyDown)
        self.registerEvent(pyui2.locals.CHAR, self._pyui2Char)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONUP, self._pyui2MouseUp)
        self.registerEvent(pyui2.locals.MOUSEMOVE, self._pyui2MouseMotion)
        self.registerEvent(pyui2.locals.CLICKED, self._pyui2Clicked)

    def getPreferredSize(self):
        #font = getTheme().getProperty("DEFAULT FONT")
        size = self.font.getTextSize("W" * self.maxSize)
        return size[0], int(size[1] * 1.5) 

    def getMaximumSize(self):
        return Much, self.getPreferredSize()[1]

    def setText(self, text):
        """external function to set the text and move the caret to the end"""
        if not text:
            self.text = ""
            self.caretPos = 0
            self.selectPos = 0
            return
        self.text = text
        self.caretPos = len(text)
        self.selectPos = self.caretPos
        self.setDirty()

    def loseFocus(self):
        Base.loseFocus(self)
        self.caretPos = 0
        self.selectPos = 0

    def getFocus(self):
        Base.getFocus(self)
        self.selectPos = len(self.text)
        self.caretPos = len(self.text)

    def findMousePos(self, pos):
        # put hit position in window relative coords
        x = pos[0] - self.posX
        #print pos[0], x
                
        # find the horizontal position within the text by binary search
        caret,r = 0, len(self.text)
        c = 0

        cnum = 0
        cx = 0
        for ch in self.text:
            #print "Char =", ch
            cw = self.font.getTextSize(ch)[0]
            if cx <= x < (cx + cw):
                #print "          ", self.text[0:cnum+1], " width =", self.font.getTextSize(self.text[0:cnum+1])[0]
                #print "           cw =", cw, "cx <= x < (cx + cw) =", cx, x, (cx + cw)
                caret = cnum
                break

            cnum += 1
            cx = cx + cw

        #print "The caret is at:", caret
        return caret


#        while l < r:
#            c = (l + r + 1) / 2
#            w = self.font.getTextSize(self.text[l:c])[0]
#            if x >= w:
#                l = c
#                x -= w
#            else:
#                if r == c:
#                    if x > w / 2:
#                        l = l + 1
#                    break
#                r = c
#        return l                
        
    def _pyui2MouseDown(self, event):
        if not self.hit(event.pos):
            return 0

        adjEvtPos = self.convertToWindowCoords(event.pos)

        self.getFocus()
        self.caretPos = self.findMousePos(adjEvtPos)
        self.selectPos = self.caretPos
        self.dragging = 1
        self.setDirty()
        return 1

    def _pyui2MouseMotion(self, event):
        if not self.dragging:
            return 0

        adjEvtPos = self.convertToWindowCoords(event.pos)

        self.caretPos = self.findMousePos(adjEvtPos)
        self.setDirty()
        return 1

    def _pyui2MouseUp(self, event):
        if not self.dragging:
            return 0

        adjEvtPos = self.convertToWindowCoords(event.pos)

        self.caretPos = self.findMousePos(adjEvtPos)
        self.dragging = 0
        self.setDirty()
        return 1

    def _pyui2Clicked(self, event):
        if event.id == self.id:
            ret = 0
            if self.handler:
                ret = self.handler(self)
            # Should we clear the text here??
            #self.setText("")
            return ret

    def deleteSelected(self):
        if self.selectPos == self.caretPos:
            return
        if self.caretPos > self.selectPos:
            (self.caretPos, self.selectPos) = (self.selectPos, self.caretPos)

        self.text = self.text[:self.caretPos] + self.text[self.selectPos:]
        self.setDirty()
        self.selectPos = self.caretPos

    def _pyui2KeyDown(self, event):
        if not self.hasFocus():
            return 0

        if event.key == pyui2.locals.K_LEFT:
            if self.caretPos > 0:
                self.caretPos -= 1
            if (event.mods & pyui2.locals.MOD_CONTROL):
                while self.caretPos > 0 and self.text[self.caretPos - 1].isspace():
                    self.caretPos -= 1
                while self.caretPos > 0 and not self.text[self.caretPos - 1].isspace():
                    self.caretPos -= 1
            if not (event.mods & pyui2.locals.MOD_SHIFT):
                self.selectPos = self.caretPos
            self.setDirty()
            return 1

        if event.key == pyui2.locals.K_RIGHT:
            if self.caretPos < len(self.text):
                self.caretPos += 1
            if (event.mods & pyui2.locals.MOD_CONTROL):
                while self.caretPos < len(self.text) and not self.text[self.caretPos].isspace():
                    self.caretPos += 1
                while self.caretPos < len(self.text) and self.text[self.caretPos].isspace():
                    self.caretPos += 1
            if not (event.mods & pyui2.locals.MOD_SHIFT):
                self.selectPos = self.caretPos
            self.setDirty()
            return 1

        if event.key == pyui2.locals.K_HOME:
            self.caretPos = 0
            if not (event.mods & pyui2.locals.MOD_SHIFT):
                self.selectPos = self.caretPos
            self.setDirty()
            return 1

        if event.key == pyui2.locals.K_END:
            self.caretPos = len(self.text)
            if not (event.mods & pyui2.locals.MOD_SHIFT):
                self.selectPos = self.caretPos
            self.setDirty()
            return 1

        # do not allow modification if edit is read-only
        if self.readOnly:
            return 0

        if event.key == pyui2.locals.K_BACKSPACE:
            if self.selectPos != self.caretPos:
                self.deleteSelected()
            elif self.caretPos > 0:
                self.text = self.text[:self.caretPos-1] + self.text[self.caretPos:]
                self.caretPos -= 1
                self.selectPos = self.caretPos
            self.setDirty()
            return 1

        if event.key == pyui2.locals.K_DELETE:
            if self.selectPos != self.caretPos:
                self.deleteSelected()
            elif self.caretPos < len(self.text):
                self.text = self.text[:self.caretPos] + self.text[self.caretPos+1:]
                self.selectPos = self.caretPos
            self.setDirty()
            return 1

        if event.key == pyui2.locals.K_RETURN:
            # invoke handler
            self.postEvent(pyui2.locals.CLICKED)
            return 1

        # handle key presses - these are really handled by onChar
        #if event.key >= 32 and event.key < 128:
        #   # add regular text to the box
        #   self.text = self.text[:self.caretPos] + chr(event.key) + self.text[self.caretPos:]
        #   self.caretPos += 1
        #   self.selectPos = self.caretPos
        #   self.setDirty()
        #   return 1
        
        return 0

    def _pyui2Char(self, event):
        if not self.hasFocus():
            return 0

        # do not allow modification if edit is read-only
        if self.readOnly:
            return 0
        
        if ord(event.key) < 32 or ord(event.key) > 128:
            return 0

        if self.caretPos != self.selectPos:
            self.deleteSelected()

        if len(self.text) > self.maxSize:
            return 1

        # add regular text to the box
        self.text = self.text[:self.caretPos] + event.key + self.text[self.caretPos:]
        self.caretPos += 1
        self.selectPos = self.caretPos
        self.setDirty()
        return 1

class NumberEdit(Edit):
    """I am an edit box that will only take numbers as input.  I will only allow
    decimel points if asked to, and will only allow the first character to be a minus sign.
    """

    widgetLabel = "NumberEdit"

    def __init__(self,text, maxSize, handler, allowDecimels):

        Edit.__init__(self, text, maxSize, handler)

        self.allowDecimels = allowDecimels
        self.getValue()   # just check the initial data to see if it's legal
        
    def _pyui2Char(self, event):
        if not self.hasFocus():
            return 0
                
        ordValue = ord(event.key)
        if ordValue < 45 or ordValue == 47 or ordValue > 57:
            return 0

        if ordValue == 45 and len(self.text) != 0:
            return 0  # only the first character can be a minus sign.

        if ordValue == 46:  # only one decimel point allowed.
            if self.allowDecimels == 0:
                return 0
            
            for char in self.text:
                if char == '.':
                    return 0

        return Edit._pyui2Char(self, event)    

    def getValue(self):
        """Returns the integer or real version of this data.
        """
        if self.text == "":
            self.text = "0"
            self.setDirty()            
        
        try:
            if self.allowDecimels:
                return float(self.text)
            else:
                return int(self.text)
        except ValueError:
            raise 'NumberEdit got an invalid value in it somehow ("' + self.text + '")'
            return 0

    def setValue(self, value):
        try:
            self.setText(str(value))
        except:
            raise 'NumberEdit could not convert value to string'
    

class PasswordEdit(Edit):

    widgetLabel = "Password"       

#    def draw(self, renderer):
#        hidden = len(self.text) * "*"
#        getPresenter().draw("EDIT", self.windowRect, (hidden, self.hasFocus(), self.caretPos, self.selectPos))

