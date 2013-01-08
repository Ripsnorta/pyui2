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

#############################################################################################################
##
#############################################################################################################
class LabelPanel(WidgetDemoPanel):

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, owner):
        WidgetDemoPanel.__init__(self, owner)

        self.controlGroup.addChild(pyui2.widgets.CheckBox("Shadowed", self.onLabelShadowed), (0, 1, 3, 1))
        self.controlGroup.addChild(pyui2.widgets.CheckBox("Bordered", self.onLabelBordered), (0, 2, 3, 1))

        self.controlGroup.addChild(pyui2.widgets.Label("Justification:"),                    (0, 4, 3, 1))
        
        justGroup = pyui2.widgets.RadioGroup(self.onJustification)
        self.controlGroup.addChild(pyui2.widgets.RadioButton("Left", justGroup),             (3, 4, 2, 1))
        self.controlGroup.addChild(pyui2.widgets.RadioButton("Centered", justGroup),         (6, 4, 3, 1))
        self.controlGroup.addChild(pyui2.widgets.RadioButton("Right", justGroup),            (9, 4, 2, 1))

        self.controlGroup.addChild(pyui2.widgets.Label("Set Text:"),                         (0, 6, 3, 1))
        self.controlGroup.addChild(pyui2.widgets.Edit("Label 1", 15),                        (3, 6, 3, 1))
        self.controlGroup.addChild(pyui2.widgets.Button("Set Label", self.onSetLabel),       (6, 6, 2, 1))

        label = pyui2.widgets.Label("Label 1", None, None, 0)
        self.widgetGroup.addChild(label, (9, 4, 3, 1))
        self.completeInit()


    #########################################################################################################
    ##
    #########################################################################################################
    def onJustification(self, value):
        label = self.widgetGroup.getWidget("LABEL_0")
        if value == 0:
            logText = "Label has been left justified"
            label.setAlignment(0)
        elif value == 1:
            logText = "Label has been centered"
            label.setAlignment(1)
        elif value == 2:
            logText = "Label has been right justified"
            label.setAlignment(2)
        else:
            logText = "Justification radio button returned incorrect value"

        self.owner.addToLog(logText)



    #########################################################################################################
    ##
    #########################################################################################################
    def onLabelShadowed(self, data):
        label = self.widgetGroup.getWidget("LABEL_0")
        if label == None:
            self.owner.addToLog("Misidentified widget")
            return

        if data == 0:
            label.setShadow(False)
            text = "Turning the shadow for the label off"
        else:
            label.setShadow(True)
            text = "Turning on the shadow for the label"

        self.owner.addToLog(text)

    #########################################################################################################
    ##
    #########################################################################################################
    def onLabelBordered(self, data):
        label = self.widgetGroup.getWidget("LABEL_0")
        if label == None:
            self.owner.addToLog("Misidentified widget")
            return

        if data == 0:
            label.setBorder(False)
            text = "Turning the border for the label off"
        else:
            label.setBorder(True)
            text = "Turning on the border for the label"

        self.owner.addToLog(text)

    #########################################################################################################
    ##
    #########################################################################################################
    def onSetLabel(self, data):
        label = self.widgetGroup.getWidget("LABEL_0")
        if label == None:
            self.owner.addToLog("Misidentified widget")
            return

        edit = self.controlGroup.getWidget("EDIT_0")
        if edit == None:
            self.owner.addToLog("Misidentified widget")
            return

        label.setText(edit.text)