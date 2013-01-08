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

import random
import pyui2
from widgetdemopanel import WidgetDemoPanel


READWRITE = 0
READONLY = 1

#############################################################################################################
##
#############################################################################################################
class GridPanel(WidgetDemoPanel):

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, owner):
        WidgetDemoPanel.__init__(self, owner)
        gp = pyui2.widgets.GridPanel(8, 6)

        for i in range(0,5):
            gp.putCellAt( pyui2.widgets.Button("button #%d" % i, None),     random.randrange(0,8), random.randrange(0,6) )
            gp.putCellAt( pyui2.widgets.Label("label #%d" % i),             random.randrange(0,8), random.randrange(0,6) )
            gp.putCellAt( pyui2.widgets.Edit("edit #%d" % i, 12, None),     random.randrange(0,8), random.randrange(0,6) )
            gp.putCellAt( pyui2.widgets.SliderBar(self.onSlider, 50, 30),   random.randrange(0,8), random.randrange(0,6) )

        self.widgetGroup.addChild(gp, (0, 0, 21, 9))
        self.completeInit()

    def onSlider(self, data):
        pass