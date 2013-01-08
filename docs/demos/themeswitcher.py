###################################################################################
# Copyright (c) 2005 John Judd
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###################################################################################

import pyui2
from optparse import OptionParser

from pyui2.desktop import getDesktop, getTheme

from pyui2.themes import Theme
from pyui2.themes import Win2kTheme
from pyui2.themes import WinXPTheme
from pyui2.themes import OSXTheme
from pyui2.themes import ComicTheme



class ThemeSwitcher:

    frame = None


    def init(self, sx, sy, deviceName):
        pyui2.init(sx, sy, deviceName, 0, "Test Window")

        self.themes = { "Standard" : Theme,
                        "Windows 2000" : Win2kTheme,
                        "Windows XP" : WinXPTheme,
                        "Mac OSX" : OSXTheme,
                        "Comic" : ComicTheme,
                      }

        self.themeTitle = "Standard Theme"


    def setCurrentTheme(self, themeName):
        self.currentTheme = themeName

        SelectedTheme = self.themes[themeName]

        pyui2.desktop.setTheme(SelectedTheme())

        self.themeTitle = themeName + " Theme"

        if self.frame:
            self.frame.setTitle(self.themeTitle)


    def onThemeChange(self, menuitem):
        self.setCurrentTheme(menuitem.text)


    def onOpenTabs(self, arg):
        self.tabbedFrame = pyui2.widgets.Frame(150, 150, 250, 200, "Tabbed Frame")

        self.tabPanel = pyui2.widgets.TabbedPanel()

        for title in ("Tab 1", "Tab 2", "Tab 3"):
            self.tabPanel.addPanel(title)

        self.tabbedFrame.replacePanel(self.tabPanel)

        self.tabPanel.getPanel(0).setLayout(pyui2.layouts.GridLayoutManager(2,4))
        self.tabPanel.getPanel(1).setLayout(pyui2.layouts.GridLayoutManager(2,4))
        self.tabPanel.getPanel(2).setLayout(pyui2.layouts.GridLayoutManager(2,4))

        self.tabbedFrame.pack()

    def onCheckbox(self, data):
        pass
        #print "Checkbox clicked with data = ", data

    def run(self):
        parser = OptionParser()
        parser.add_option("-D", action="store", type="string", dest="deviceName", default="2d")
        (options, args) = parser.parse_args()
        #print options.deviceName

        self.init(800, 600, options.deviceName)

        menu1 = pyui2.widgets.Menu("Themes")
        for item in self.themes:
            menu1.addItem(item, self.onThemeChange)

        self.mbar = pyui2.widgets.MenuBar()
        self.mbar.addMenu(menu1)

        self.frame = pyui2.widgets.Frame(40, 40, 720, 520, self.themeTitle)
        self.frame.setLayout(pyui2.layouts.TableLayoutManager(21, 21))

        btn = pyui2.widgets.Button("Open Tabs", self.onOpenTabs)

        lb_items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9"]
        lb = pyui2.widgets.ListBox()
        lb.populateList(lb_items)

        dd_items = [("Item 1", None), ("Item 2", None), ("Item 3", None), ("Item 4", None), ("Item 5", None)]
        dd = pyui2.widgets.DropDownBox(3, None, dd_items)

        pic = pyui2.widgets.Picture("../../images/cursor_drag.png")
        ib1 = pyui2.widgets.ImageButton("../../images/cursor_wait.png", None)
        ib2 = pyui2.widgets.ImageButton("../../images/cursor_hand.png", None)
        ib3 = pyui2.widgets.ImageButton("../../images/cursor_resize.png", None)

        lbl1 = pyui2.widgets.Label("Label 1", None, None, 0)
        lbl2 = pyui2.widgets.Label("Label 2", None, None, 1)

        cb1 = pyui2.widgets.CheckBox("CheckBox 1", self.onCheckbox)
        cb2 = pyui2.widgets.CheckBox("CheckBox 2", None)
        cb2.setID("Happy Fun Time")
        cb3 = pyui2.widgets.CheckBox("CheckBox 3", None, 1)

        READWRITE = 0
        READONLY = 1

        eb1 = pyui2.widgets.Edit("Edit 1", 5, None, READONLY)
        eb2 = pyui2.widgets.Edit("some text for this edit", 10, None, READWRITE)
        eb3 = pyui2.widgets.Edit("Another lot of text", 7, None)

        slb = pyui2.widgets.SliderBar(None, 6, 3)

        self.frame.addChild(btn, (10, 20, 3, 1))
        self.frame.addChild(pic, (1, 1, 2, 2))
        self.frame.addChild(ib1, (3, 1, 2, 2))
        self.frame.addChild(ib2, (5, 1, 2, 2))
        self.frame.addChild(ib3, (7, 1, 2, 2))
        self.frame.addChild(lbl1, (1, 4, 3, 1))
        self.frame.addChild(lbl2, (4, 4, 3, 1))
        self.frame.addChild(cb1, (1, 6, 3, 1))
        self.frame.addChild(cb2, (1, 7, 3, 1))
        self.frame.addChild(cb3, (1, 8, 3, 1))
        self.frame.addChild(eb1, (5, 6, 2, 1))
        self.frame.addChild(eb2, (5, 7, 2, 1))
        self.frame.addChild(eb3, (5, 8, 2, 1))
        self.frame.addChild(dd, (11, 1, 4, 1))
        self.frame.addChild(lb, (15, 1, 5, 5))
        self.frame.addChild(slb, (1, 10, 6, 1))
        self.frame.pack()

        pyui2.run()
        pyui2.quit()


if __name__ == '__main__':
    app = ThemeSwitcher()
    app.run()
