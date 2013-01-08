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
#
import pyui2
from pyui2.desktop import getPresenter
from pyui2.system import DCX
from pyui2.system import Pen, Brush


class DCXTest:

    def init(self, sx, sy):
        pyui2.init(sx, sy, "2d", 0, "DCX Test Window")

    def callback(self):
        # Set up a gray, solid pen
        p = pyui2.system.Pen(1, (192, 192, 192, 255), Pen.STYLE_SOLID)

        # Draw a line using the pen with two points in the point list
        self.gc.drawLine(((10, 10), (390, 10)), p)

        # Draw a line using the pen with three points in the point list
        self.gc.drawLine(((10, 20), (100, 20), (100, 50)), p)

        # Draw a rectangle
        self.gc.drawRect((10, 40, 100, 30), p)

        # Draw a filled rectangle with a solid brush
        b1 = pyui2.system.Brush((255, 0, 0, 255), Brush.STYLE_SOLID)
        self.gc.drawFilledRect((150, 40, 100, 30), b1)

        # Draw a circle
        p2 = pyui2.system.Pen(1, (255, 0, 0, 255), Pen.STYLE_SOLID)
        self.gc.drawCircle((60, 140), 50, p2)

        # Draw a filled circle
        b2 = pyui2.system.Brush((0, 255, 0, 255), Brush.STYLE_SOLID)
        self.gc.drawFilledCircle((180, 140), 50, b2)

        # Draw a filled circle
        b3 = pyui2.system.Brush((0, 0, 255, 255), Brush.STYLE_SOLID)
        self.gc.drawFilledCircle((300, 140), 50, b3)

        outlinePen = pyui2.system.Pen(3, (255, 255, 255, 255), Pen.STYLE_SOLID)
        brush = pyui2.system.Brush((192, 192, 222, 255), Brush.STYLE_SOLID)

        rect = pyui2.system.Rectangle((10, 250, 80, 30), outlinePen, brush)
        self.gc.drawGraphicObject(rect)

        square = pyui2.system.Square((10, 300), 50, outlinePen, brush)
        self.gc.drawGraphicObject(square)

        circle = pyui2.system.Circle((180, 300), 50, outlinePen, brush)
        self.gc.drawGraphicObject(circle)

        line = pyui2.system.Line(((250, 250), (275, 300), (300, 250), (325, 300)), outlinePen)
        self.gc.drawGraphicObject(line)

        polygon = pyui2.system.Polygon(((340, 250), (390, 250), (365, 300)), outlinePen, brush)
        self.gc.drawGraphicObject(polygon)


        self.gc.render((100, 100))
        self.dc.present()

    def run(self):
        self.init(800, 600)

        self.dc = getPresenter().getDeviceContext()

        self.gc = self.dc.createGraphicsContext((400, 400))

        getPresenter().setBackgroundDrawing(self.callback)

        pyui2.run()
        pyui2.quit()


if __name__ == '__main__':
    test = DCXTest()
    test.run()
