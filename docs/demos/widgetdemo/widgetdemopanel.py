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
from pyui2.widgets import Panel



#############################################################################################################
##
#############################################################################################################
class WidgetDemoPanel(Panel):

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, owner):
        Panel.__init__(self)

        self.owner = owner

        self.setLayout(pyui2.layouts.GridLayoutManager(1, 2))

        self.controlGroup = pyui2.widgets.Group()
        self.controlGroup.setLayout(pyui2.layouts.TableLayoutManager(21, 9))

        self.widgetGroup = pyui2.widgets.Group()
        self.widgetGroup.setLayout(pyui2.layouts.TableLayoutManager(21, 9))

        self.addChild(self.controlGroup)
        self.addChild(self.widgetGroup)

    #########################################################################################################
    ##
    #########################################################################################################
    def completeInit(self):
        self.controlGroup.pack()
        self.widgetGroup.pack()
        self.pack()
