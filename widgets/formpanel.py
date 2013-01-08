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

import pyui2

from pyui2.desktop import getDesktop, getTheme
from pyui2.panel import Panel
from pyui2.layouts import Much


class FormPanel(Panel):
    """A Panel that shows data about an object and allows it to be updated.
    The "fields" argument is a list of data fields to populate the panel with. It
    is in the format:
       [ (type, name, label, vspan, data),
         (type, name, label, vspan, data)
       ]

    where type is one the fieldTypes below, vspan is the vertical height of the widget,
    and data is speficic data for the type of form widget to be used.
    """

    fieldTypes = [
        "string",
        "int",
        "float",
        "text",
        "password",
        "slider",
        "checkbox",
        "list",
        "dropdownlist",
        "label"
        ]
    
    def __init__(self, fieldList):
        self.fieldList = fieldList
        Panel.__init__(self)
        self.object = None
        # setup layout
        num = 0

        span = 0
        for t, n, l, vspan, d in fieldList:
            span = span + vspan
            
        self.setLayout(pyui2.layouts.TableLayoutManager( 3, span))
        for fieldType, fieldName, fieldLabel, fieldSpan, fieldData in fieldList:
            newLabel = Label(fieldLabel)
            newWidget = self.createFormWidget(fieldType, fieldData)
            self.addChild( newLabel, (0,num,1,fieldSpan) )
            self.addChild( newWidget, (1,num,2,fieldSpan) )

            self.__dict__["label_%s" % fieldName] = newLabel
            self.__dict__["widget_%s" % fieldName] = newWidget
            
            num = num + fieldSpan
        self.pack()

    def populate(self, object):
        """populate the data fields from the supplied object
        """
        self.object = object
        for fieldType, fieldName, fieldLabel, fieldSpan, fieldDefault in self.fieldList:
            formWidget = self.__dict__["widget_%s" % fieldName]
            value = object.__dict__.get(fieldName, None)
            self.populateFormWidget(fieldType, formWidget, value)
        self.setDirty(1)

    def process(self):
        """This takes the data in the form and updates it into the source object.
        This assumes that the form has already been populated...
        """
        for fieldType, fieldName, fieldLabel, fieldSpan, fieldData in self.fieldList:
            formWidget = self.__dict__["widget_%s" % fieldName]
            self.processFormWidget(fieldType, fieldName, formWidget)
        
    def createFormWidget(self, fieldType, fieldData):
        """Create the right kind of widget based on the fieldType.
        """
        tmp = "create_%s" % fieldType
        createMethod = getattr(self, tmp)
        if not createMethod:
            raise "No widget of type: %s" % tmp
        return createMethod(fieldData)

    def populateFormWidget(self, fieldType, formWidget, value):
        tmp = "populate_%s" % fieldType
        populateMethod = getattr(self, tmp)
        if not populateMethod:
            raise "No widget of type: %s" % fieldType
        return populateMethod(formWidget, value)

    def processFormWidget(self, fieldType, fieldName, formWidget):
        if not self.object:
            raise "No object to process to!"
        tmp = "process_%s" % fieldType
        processMethod = getattr(self, tmp)
        if not processMethod:
            raise "No process method for %s" % fieldType
        return processMethod(formWidget, fieldName)
    
    ##### Widget Creation Methods. #####
    
    def create_string(self, size):
        return Edit("", size, self._pyui2Edit)

    def create_password(self, size):
        return Password("", size, self._pyui2Edit)

    def create_int(self, dummy):
        return NumberEdit("", 12, self._pyui2Edit, 0)

    def create_float(self, dummy):
        return NumberEdit("", 12, self._pyui2Edit, 0)

    def create_text(self, size):
        #NOTE: make this a LineDisplay that can be edited...
        return Edit("", size, self._pyui2Edit)

    def create_slider(self, range):
        return SliderBar(self._pyui2Slide, range)

    def create_checkbox(self, title):
        return CheckBox(title, self._pyui2Check)
    
    def create_list(self, dummy):
        return ListBox()

    def create_dropdownlist(self, numVisible):
        return DropDownBox(numVisible)

    def create_label(self, dummy):
        return Label("")
    
    ###### Widget Populate Methods. #######

    def populate_string(self, formWidget, value):
        if not value:
            formWidget.setText("None")
        else:
            formWidget.setText("%s" % value)

    def populate_float(self, formWidget, value):
        if not value:
            formWidget.setText("None")
        else:
            formWidget.setText("%.2f" % value)
        
    populate_password = populate_string
    populate_int = populate_string
    populate_text = populate_string
    populate_label = populate_string
    
    def populate_slider(self, formWidget, value):
        formWidget.position = value

    def populate_checkbox(self, formWidget, value):
        formWidget.setCheck(value)
        
    def populate_list(self, formWidget, items):
        #TODO: make a way to get a text value for an item
        formWidget.clear()
        for item in items:
            formWidget.addItem(repr(item), item)

    populate_dropdownlist = populate_list

    ##### Widget Processing Methods #####

    def process_string(self, formWidget, fieldName):
        setattr(self.object, fieldName, formWidget.text)

    process_text = process_string
    process_password = process_string

    def process_label(self, formWidget, fieldName):
        pass

    def process_list(self, formWidget, fieldName):
        pass

    process_dropdownlist = process_list

    def process_slider(self, formWidget, fieldName):
        setattr(self.object, fieldName, formWidget.position)

    def process_checkbox(self, formWidget, fieldName):
        setattr(self.object, fieldName, formWidget.checkState)
        
    def process_int(self, formWidget, fieldName):
        setattr(self.object, fieldName, int(formWidget.text) )
        
    def process_float(self, formWidget, fieldName):
        setattr(self.object, fieldName, float(formWidget.text) )

    ##### Widget handler methods ######
    
    def _pyui2Slide(self, value):
        #print "slid to ", value
        pass
            
    def _pyui2Edit(self, edit):
        #print "changing value for ", edit
        return 1

    def _pyui2Check(self, value):
        #print "checkbox hit"
        pass
