# pyui2
# Copyright (C) 2005 John Judd
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

import types
import pyui2

import pyui2.system
from pyui2.themes import ThemeBase
from pyui2.system import GCX


class Theme(ThemeBase):
    def __init__(self):
        ThemeBase.__init__(self)

    def setupTheme(self):
        #print "Setting up the theme"
        ThemeBase.setupTheme(self)


        self.setProperty("DEFAULT FONT", pyui2.system.Font("tahoma", 14, 0))

        windowProp = self.getProperty("WINDOW")
        windowProp.setProperty("background", pyui2.system.Brush((255, 255, 255, 255), pyui2.system.Brush.STYLE_SOLID))

        panelProp = self.getProperty("PANEL")
        panelProp.setProperty("background", pyui2.system.Brush((180, 180, 180, 180), pyui2.system.Brush.STYLE_SOLID))


        frameProp = self.getProperty("FRAME")
        frameProp.setProperty("background", pyui2.system.Brush((200, 200, 200, 255), pyui2.system.Brush.STYLE_SOLID))

        borderProp = frameProp.getProperty("BORDER")
        borderProp.setProperty("width", 4)
        borderProp.setProperty("color", (0, 0, 190, 255))

        captionBarProp = self.getProperty("CAPTIONBAR")
        captionBarProp.setProperty("background", pyui2.system.Brush((0, 0, 140, 255), pyui2.system.Brush.STYLE_SOLID))

        titleProp = captionBarProp.getProperty("TITLE")
        titleProp.setProperty("justified", "left")
        titleProp.setProperty("font", pyui2.system.Font("tahoma", 14, 0))

        buttonProp = captionBarProp.getProperty("BUTTONS")
        buttonProp.setProperty("justified", "right")



        closeButtonProp = self.getProperty("CLOSEBUTTON")
        closeBtnPen1 = pyui2.system.Pen(2, (128, 128, 128, 255), pyui2.system.Pen.STYLE_SOLID)
        closeBtnPen2 = pyui2.system.Pen(3, (0, 0, 0, 255), pyui2.system.Pen.STYLE_SOLID)
        closeBtnBrush = pyui2.system.Brush((192, 192, 192, 255), pyui2.system.Brush.STYLE_SOLID)
        cbCircle = pyui2.system.Circle(None, None, closeBtnPen1, closeBtnBrush)
        cbCross = pyui2.system.Line(((5, 5), (11, 11), (8, 8), (11, 5), (5, 11)), closeBtnPen2)
        closeButtonProp.setProperty("drawlist", (cbCircle, cbCross))

        minButtonProp = self.getProperty("MINBUTTON")

        maxButtonProp = self.getProperty("MAXBUTTON")



        labelProp = self.getProperty("LABEL")
        labelProp.setProperty("color", (0, 0, 0, 255))
        labelProp.setProperty("shadowcolor", (128, 128, 128, 255))

        buttonProp = self.getProperty("BUTTON")
        buttonProp.setProperty("color", (192, 192, 192, 255))

        imgBtnProp = self.getProperty("IMAGEBUTTON")

        checkProp = self.getProperty("CHECKBOX")
        checkProp.setProperty("font", pyui2.system.Font("tahoma", 12, 0))

        editProp = self.getProperty("EDIT")
        editProp.setProperty("font", pyui2.system.Font("tahoma", 12, 0))

        sliderProp = self.getProperty("SLIDERBAR")

        scrollProp = self.getProperty("SCROLLBAR")
        scrollProp.setProperty("scrollersize", 14)

        tabPanelProp = self.getProperty("TABPANEL")

        menuBarProp = self.getProperty("MENUBAR")

        menuProp = self.getProperty("MENU")

        listboxProp = self.getProperty("LISTBOX")
        listboxProp.setProperty("function", self.drawListBox)

        dropdownProp = self.getProperty("DROPDOWN")

        splitterProp = self.getProperty("SPLITTER")

        tooltipProp = self.getProperty("TOOLTIP")

        pictureProp = self.getProperty("PICTURE")

        #self.printPropertyTree(self.properties)


