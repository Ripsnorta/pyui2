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
from themesetup import setupTestTheme


def onList1(arg):
	print "got a button " 

def onList2(arg):
	print "got a button " 

def onList3(arg):
	print "got a button " 
	
def run():
	setupTestTheme(800, 600)

	list1 = [("Item 1", None), ("Item 2", None), ("Item 3", None)]
	list2 = [("Apples", None), ("Oranges", None), ("Bananas", None), ("Plums", None)]
	list3 = [("Star Trek", "Good"), ("Stargate: SG1", "Great"), ("Babylon 5", "The Greatest")]

	w = pyui2.widgets.Frame(50, 50, 400, 400, "Dropdown Box Test")
	w.addChild(pyui2.widgets.DropDownBox(3, onList1, list1))
	w.addChild(pyui2.widgets.DropDownBox(3, onList2, list2, 1))
	w.addChild(pyui2.widgets.DropDownBox(3, onList3, list3, 2))
	w.pack()

	pyui2.run()
	pyui2.quit()


if __name__ == '__main__':
	run()
