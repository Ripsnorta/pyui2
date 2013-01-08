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

    
class ColorDialog(Dialog):
    """Allows the user to select a color.
    """
    def __init__(self, callback, r=255, g=0, b=0):
        self.callback = callback
        self.r = r
        self.g = g
        self.b = b
        
        Dialog.__init__(self, -1, -1, 400,240, "Color Dialog")
        self.setLayout(pyui2.layouts.TableLayoutManager(4,9))

        self.colorGradient = ColorGradient(None, self)
        self.colorStrip = ColorStrip(None, self)
        self.colorSolid = ColorSolid(None)

        self.okButton = pyui2.widgets.Button("OK", self._pyui2OK)
        self.cancelButton = pyui2.widgets.Button("Cancel", self._pyui2Cancel)
        
        self.redLabel = pyui2.widgets.Label("Red:")
        self.greenLabel = pyui2.widgets.Label("Green:")
        self.blueLabel = pyui2.widgets.Label("Blue:")

        self.redBox = pyui2.widgets.SliderBar(self._pyui2Red, 255, r)
        self.greenBox = pyui2.widgets.SliderBar(self._pyui2Green, 255, g)
        self.blueBox = pyui2.widgets.SliderBar(self._pyui2Blue, 255, b)

        self.addChild( self.colorGradient,  (0,0,2,5) )
        self.addChild( self.colorStrip,     (2,0,2,5) )
        self.addChild( self.colorSolid,     (0,5,1,3) )
        self.addChild( self.redLabel,       (1,5,1,1) )
        self.addChild( self.greenLabel,     (1,6,1,1) )
        self.addChild( self.blueLabel,      (1,7,1,1) )        
        self.addChild( self.redBox,         (2,5,2,1) )
        self.addChild( self.greenBox,       (2,6,2,1) )
        self.addChild( self.blueBox,        (2,7,2,1) )        
        self.addChild( self.cancelButton,   (0,8,2,1) )
        self.addChild( self.okButton,       (2,8,2,1) )        

        self.pack()
        self.setColor()
        
    def setColor(self, strip=1):
        self.color = (self.r,self.g,self.b, 255)
        self.colorSolid.color = self.color
        if strip:
            self.colorStrip.color = self.color
        self.setDirty(1)
        
    def _pyui2OK(self, button):
        self.callback(self.color)
        self.close(1)

    def _pyui2Cancel(self, button):
        self.close(0)

    def _pyui2Red(self, value):
        self.r = value
        self.setColor()

    def _pyui2Green(self, value):
        self.g = value
        self.setColor()
        pass

    def _pyui2Blue(self, value):
        self.b = value
        self.setColor()

    def setRGB(self, r, g, b,strip=1):
        self.r = r
        self.g = g
        self.b = b
        self.redBox.setValue(r)
        self.greenBox.setValue(g)
        self.blueBox.setValue(b)        
        self.setColor(strip)
    
class ColorSolid(pyui2.widgets.Base):
    def __init__(self, color):
        pyui2.widgets.Base.__init__(self)
        self.color = color

#    def draw(self, renderer):
#        renderer.drawRect(pyui2.colors.black, self.windowRect)
#        renderer.drawRect(self.color, (self.windowRect[0]+2,self.windowRect[1]+2,self.windowRect[2]-4,self.windowRect[3]-4) )

class ColorGradient(pyui2.widgets.Base):

    colors = [
        (255,0,0),
        (255,255,0),
        (0,255,0),
        (0,255,255),
        (0,0,255),
        (255,0,255),
        (255,0,0)
        ]

    segments = 6
    
    def __init__(self, color, dialog):
        pyui2.widgets.Base.__init__(self)
        self.color = color
        self.dialog = dialog
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)         

#    def draw(self, renderer):
#        renderer.drawRect(pyui2.colors.black, self.windowRect)
#        top = self.windowRect[1]+2
#        height = self.windowRect[3]-4
#        width = self.windowRect[2] / float(self.segments)
#        for i in range(0,self.segments):
#            renderer.drawGradient( (self.windowRect[0]+int(i*width),top,int(width+1),height),
#                                   apply(renderer.packColor,self.colors[i]),
#                                  apply(renderer.packColor,self.colors[i+1]),
#                                  apply(renderer.packColor,self.colors[i]),
#                                  apply(renderer.packColor,self.colors[i+1]))
#

    def _pyui2MouseDown(self, event):
        if not self.hit(event.pos):
            return 0
        x = event.pos[0] - self.rect[0]
        ratio = float(x) / float(self.windowRect[2])
        hitSegment = int(ratio * self.segments)
        before = self.colors[hitSegment]
        after = self.colors[hitSegment+1]
        innerRatio = (ratio * self.segments) - hitSegment
        
        newColor = []
        for i in range(0,3):
            diff = after[i] - before[i]
            value = before[i] + innerRatio*diff
            newColor.append(int(value))
        apply(self.dialog.setRGB, newColor)
        return 1
    
class ColorStrip(pyui2.widgets.Base):
    def __init__(self, color, dialog):
        pyui2.widgets.Base.__init__(self)
        self.color = color
        self.dialog = dialog
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        
#    def draw(self, renderer):
#        renderer.drawRect(pyui2.colors.black, self.windowRect)
#        top = self.windowRect[1]
#
#        w = self.windowRect[2]-4
#        h = self.windowRect[3]
#        rect1 =(self.windowRect[0]+2,self.windowRect[1], w, h/2)
#        rect2 =(self.windowRect[0]+2,self.windowRect[1]+(h/2), w, h/2)
#       renderer.drawGradient(rect1, pyui2.colors.white, pyui2.colors.white, self.color, self.color )
#       renderer.drawGradient(rect2,self.color, self.color, pyui2.colors.black, pyui2.colors.black )        
#       
    def _pyui2MouseDown(self, event):
        if not self.hit(event.pos):
            return 0
        y = event.pos[1] - self.rect[1]
        ratio = 2 - (float(y) / float(self.windowRect[3]))*2

        newColor = []
        for i in range(0,3):
            if ratio <= 1.0:
                value = self.color[i] * ratio
            else:
                if self.color[i] == 0:
                    value = 255 * (ratio/2)
                elif self.color[i] == 255:
                    value = 255
                else:
                    value = self.color[i] + (255 - self.color[i]) * (ratio/2)
            newColor.append(int(value))
        newColor.append(0) # this make setRGB not reset self.color
        apply(self.dialog.setRGB, newColor)
        return 1
