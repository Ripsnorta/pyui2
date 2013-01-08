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

import pyui2.system
from pyui2.themes import ThemeBase

class ComicTheme(ThemeBase):
    """A theme that looks like a comic book!
    """
    
    def __init__(self):
        ThemeBase.__init__(self)

        
    def setupTheme(self):
        ThemeBase.setupTheme(self)
        self.setProperty("DEFAULT FONT", pyui2.system.Font("comicsansms", 14, 0))

        windowProp = self.getProperty("WINDOW")
        windowProp.setProperty("background", pyui2.system.Brush((255, 255, 0, 255), pyui2.system.Brush.STYLE_SOLID))

        panelProp = self.getProperty("PANEL")
        panelProp.setProperty("background", pyui2.system.Brush((255, 255, 180, 255), pyui2.system.Brush.STYLE_SOLID))

        frameProp = self.getProperty("FRAME")
        frameProp.setProperty("background", pyui2.system.Brush((200, 0, 0, 255), pyui2.system.Brush.STYLE_SOLID))

        borderProp = frameProp.getProperty("BORDER")
        borderProp.setProperty("width", 2)
        borderProp.setProperty("color", (0, 0, 100, 255))

        menuBarProp = self.getProperty("MENUBAR")
        menuBarProp.setProperty("framecolor", (255, 255, 180, 255))
        menuBarProp.setProperty("menucolor", (255, 255, 180, 255))
        menuBarProp.setProperty("selectcolor", (200, 0, 0, 255))
        menuBarProp.setProperty("fontcolor", (200, 0, 0, 255))
        menuBarProp.setProperty("fontselectcolor", (255, 255, 180, 255))

        menuProp = self.getProperty("MENU")
        menuProp.setProperty("framecolor", (255, 255, 180, 255))
        menuProp.setProperty("menucolor", (255, 255, 180, 255))
        menuProp.setProperty("selectcolor", (200, 0, 0, 255))
        menuProp.setProperty("fontcolor", (200, 0, 0, 255))
        menuProp.setProperty("fontselectcolor", (255, 255, 180, 255))


          
