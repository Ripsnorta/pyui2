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

class ImageButtonTest:

	def onButton1(self, arg):
		print "pressed button 1" 
		if self.btn3.enabled == 1:
			self.btn3.disable()
		else:
			self.btn3.enable()
		
	def onButton2(self, arg):
		print "pressed button 2" 
		
	def onButton3(self, arg):
		print "pressed button 3" 
		
	def run(self):
		setupTestTheme(800, 600)
	
		w = pyui2.widgets.Frame(50, 50, 400, 400, "ImageButton test")
		self.btn1 = pyui2.widgets.ImageButton("cursor_drag.png", self.onButton1)
		self.btn2 = pyui2.widgets.ImageButton("cursor_hand.png", self.onButton2)
		self.btn3 = pyui2.widgets.ImageButton("cursor_resize.png", self.onButton3, "", "cursor_pointer.png")
		w.addChild(self.btn1)
		w.addChild(self.btn2)
		w.addChild(self.btn3)
		w.pack()
	
		pyui2.run()
		pyui2.quit()


if __name__ == '__main__':
	ibt = ImageButtonTest()
	ibt.run()
