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
from pyui2.themes._testtheme import TestTheme

from pyui2.desktop import setTheme




def setupTestTheme(sx, sy):
	pyui2.init(sx, sy, "2d", 0, "Test Window")
	pyui2.desktop.setTheme(pyui2.themes._testtheme.TestTheme())
	

def run():
	setupTestTheme(800, 600)

	w = pyui2.widgets.Frame(50, 50, 400, 400, "New Theme Test")
	w.addChild(pyui2.widgets.RadioButton("RadioButton 1", None))
	w.addChild(pyui2.widgets.RadioButton("RadioButton 2", None))
	w.addChild(pyui2.widgets.RadioButton("RadioButton 3", None, 1))
	w.pack()

	pyui2.run()
	pyui2.quit()


if __name__ == '__main__':
	run()
