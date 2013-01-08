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
from optparse import OptionParser

import pyui2
from pyui2.themes import Theme
from pyui2.themes import Win2kTheme
from pyui2.themes import WinXPTheme
from pyui2.themes import OSXTheme
from pyui2.themes import ComicTheme



from labelpanel import LabelPanel
from buttonpanel import ButtonPanel
from checkboxpanel import CheckboxPanel
from editpanel import EditPanel
from gridpanel import GridPanel
from sheetpanel import SheetPanel
from treepanel import TreePanel
from picturepanel import PicturePanel
from listboxpanel import ListboxPanel
from sliderbarpanel import SliderBarPanel
#from menupanel import MenuPanel
#from captionbarpanel import CaptionBarPanel
from scrollpanel import ScrollPanel
from dropdownpanel import DropdownPanel
from radiopanel import RadioPanel
from splitterpanel import SplitterPanel





#############################################################################################################
##
#############################################################################################################
class WidgetDemo:

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self):
        parser = OptionParser()
        parser.add_option("-D", action="store", type="string", dest="deviceName", default="2d")
        parser.add_option("-F", action="store_true", dest="fullscreen", default=False)
        (options, args) = parser.parse_args()

        pyui2.init(800, 600, options.deviceName, options.fullscreen, "Widget Demo")

        self.themes = { "Standard" : Theme,
                        "Windows 2000" : Win2kTheme,
                        "Windows XP" : WinXPTheme,
                        "Mac OSX" : OSXTheme,
                        "Comic" : ComicTheme,
                      }

    #########################################################################################################
    ##
    #########################################################################################################
    def setupMainFrame(self):
        flags = (pyui2.widgets.Frame.NO_CAPTION, pyui2.widgets.Frame.NO_RESIZE)
        self.mainFrame = pyui2.widgets.Frame(0, self.mbar.height, 800, 400, "", flags)

        self.tabPanel = pyui2.widgets.TabbedPanel()

        self.tabPanel.addPanel("Label",         LabelPanel(self))
        self.tabPanel.addPanel("Button",        ButtonPanel(self))
        self.tabPanel.addPanel("Checkbox",      CheckboxPanel(self))
        self.tabPanel.addPanel("Edit",          EditPanel(self))
        self.tabPanel.addPanel("Grid",          GridPanel(self))
        self.tabPanel.addPanel("Sheet",         SheetPanel(self))
        self.tabPanel.addPanel("Tree",          TreePanel(self))
        self.tabPanel.addPanel("Picture",       PicturePanel(self))
        self.tabPanel.addPanel("Listbox",       ListboxPanel(self))
        self.tabPanel.addPanel("Sliderbar",     SliderBarPanel(self))
        #self.tabPanel.addPanel("Menu",          MenuPanel(self))
        #self.tabPanel.addPanel("CaptionBar",    CaptionBarPanel(self))
        self.tabPanel.addPanel("Scroll",        ScrollPanel(self))
        self.tabPanel.addPanel("Dropdown",      DropdownPanel(self))
        self.tabPanel.addPanel("RadioButton",   RadioPanel(self))
        self.tabPanel.addPanel("Splitter",      SplitterPanel(self))

        self.mainFrame.replacePanel(self.tabPanel)
        self.mainFrame.pack()

    #########################################################################################################
    ##
    #########################################################################################################
    def setupLogFrame(self):
        flags = (pyui2.widgets.Frame.NO_CAPTION, pyui2.widgets.Frame.NO_RESIZE)
        self.logFrame = pyui2.widgets.Frame(0, self.mbar.height + 400, 800, 200 - self.mbar.height, "", flags)
        self.logFrame.setLayout(pyui2.layouts.TableLayoutManager(21, 13))
        self.logList = pyui2.widgets.ListBox()
        self.logFrame.addChild(self.logList, (0, 0, 21, 10))
        self.logFrame.addChild(pyui2.widgets.Button("Clear Log", self.onClearLog), (19, 11, 2, 2))
        self.logFrame.pack()

    #########################################################################################################
    ##
    #########################################################################################################
    def onClearLog(self, menuitem):
        self.logList.clearAllItems()

    #########################################################################################################
    ##
    #########################################################################################################
    def addToLog(self, text):
        self.logList.addItem(text, None)

    #########################################################################################################
    ##
    #########################################################################################################
    def onThemeChange(self, menuitem):
        self.currentTheme = menuitem.text
        pyui2.desktop.setTheme(self.themes[menuitem.text]())

    #########################################################################################################
    ##
    #########################################################################################################
    def onExit(self, menuitem):
        pyui2.quit()

    #########################################################################################################
    ##
    #########################################################################################################
    def setupMenu(self):
        fileMenu = pyui2.widgets.Menu("File")
        fileMenu.addItem("Exit", self.onExit)

        themeMenu = pyui2.widgets.Menu("Themes")
        for item in self.themes:
            themeMenu.addItem(item, self.onThemeChange)

        self.mbar = pyui2.widgets.MenuBar()
        self.mbar.addMenu(fileMenu)
        self.mbar.addMenu(themeMenu)

    #########################################################################################################
    ##
    #########################################################################################################
    def run(self):
        self.setupMenu()
        self.setupMainFrame()
        self.setupLogFrame()
        pyui2.run()
        pyui2.quit()


#############################################################################################################
if __name__ == '__main__':
    app = WidgetDemo()
    app.run()
