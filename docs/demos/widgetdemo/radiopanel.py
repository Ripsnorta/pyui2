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
class RadioPanel(WidgetDemoPanel):

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, owner):
        WidgetDemoPanel.__init__(self, owner)
        radGroup = pyui2.widgets.RadioGroup(self.onRadioChange)
        self.widgetGroup.addChild(pyui2.widgets.RadioButton("Radio 1", radGroup), (7, 4, 2, 1))
        self.widgetGroup.addChild(pyui2.widgets.RadioButton("Radio 2", radGroup), (10, 4, 3, 1))
        self.widgetGroup.addChild(pyui2.widgets.RadioButton("Radio 3", radGroup), (13, 4, 2, 1))
        self.completeInit()

    def onRadioChange(self, value):
        pass