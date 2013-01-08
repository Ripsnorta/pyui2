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
from widgetdemopanel import WidgetDemoPanel


READWRITE = 0
READONLY = 1

#############################################################################################################
##
#############################################################################################################
class SheetPanel(WidgetDemoPanel):

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, owner):
        WidgetDemoPanel.__init__(self, owner)
        sht = pyui2.widgets.Sheet(self.onChanged, self.onInserted)
        self.widgetGroup.addChild(sht, (0, 0, 21, 9))
        self.completeInit()

    def onChanged(self, x, y, value):
        text = "Cell (%d,%d) Set to <%s>" % ( x, y, value)
        self.owner.addToLog(text)

    def onInserted(self, x, y, value):
        text = "Cell inserted at (%d,%d), Set to <%s>" % ( x, y, value)
        self.owner.addToLog(text)
