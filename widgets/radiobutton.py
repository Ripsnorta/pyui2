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

import pyui2

from pyui2.desktop import getDesktop, getPresenter
from pyui2.base import Base
from pyui2.layouts import Much


#############################################################################################################
##
#############################################################################################################
class RadioGroup:

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, onChangeHandler=None):
        self.radioButtons = []
        self.activeButton = None
        self.onChangeHandler = onChangeHandler

    #########################################################################################################
    ##
    #########################################################################################################
    def addRadioButton(self, radioButton):
        self.radioButtons.append(radioButton)
        if self.activeButton == None:
            self.activeButton = radioButton
            self.activeButton.checkState = 1

    #########################################################################################################
    ##
    #########################################################################################################
    def buttonChecked(self, radioButton):
        if radioButton == self.activeButton:
            #Already checked
            return

        self.activeButton = radioButton
        for radio in self.radioButtons:
            if radio != self.activeButton:
                radio.setCheck(0)

        if self.onChangeHandler != None:
            self.onChangeHandler(self.getValue())

    #########################################################################################################
    ##
    #########################################################################################################
    def setValue(self, index):
        self.buttonChecked(self.radioButtons[index])

    #########################################################################################################
    ##
    #########################################################################################################
    def getValue(self):
        try:
            index = self.radioButtons.index(self.activeButton)
        except KeyError:
            index = -1

        return index

#############################################################################################################
##
#############################################################################################################
class RadioButton(Base):
    """A checkbox that has two states - on and off. It toggles between them when clicked.
    onCheck is a method to be called when the checkbox changes state.
    """

    widgetLabel = "RADIOBUTTON"

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, text, buttonGroup, onCheck = None, checked=0):
        Base.__init__(self)
        self.checkState = checked
        self.text = text
        self._pyui2Check = onCheck
        self.buttonGroup = buttonGroup
        self.buttonGroup.addRadioButton(self)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)

    #########################################################################################################
    ##
    #########################################################################################################
    def getPreferredSize(self):
        if self.font:
            font = self.font
        else:
            font = getTheme().defaultFont
        size = font.getTextSize(self.text)
        return int(size[0] * 1.5), int(size[1] * 1.5)

    #########################################################################################################
    ##
    #########################################################################################################
    def getMaximumSize(self):
        return Much, self.getPreferredSize()[1]

    #########################################################################################################
    ##
    #########################################################################################################
    def setCheck(self, value):
        if value:
            self.checkState = 1
            self.buttonGroup.buttonChecked(self)
        else:
            self.checkState = 0

        if self._pyui2Check:
            self._pyui2Check(self.checkState)

        self.setDirty(1)

    #########################################################################################################
    ##
    #########################################################################################################
    def _pyui2MouseDown(self, event):
        if not self.hit(event.pos):
            return 0

        if not self.checkState:
            self.setCheck(1)

        return 1

